const {test}=require('node:test');
const assert=require('node:assert/strict');
const E=require('../engine.js');
test('supplied gambles: 30 zero-mean pairs, exact endpoints and outcome orientation',()=>{
 assert.equal(E.GAMBLES.length,30);
 assert.deepEqual(E.GAMBLES[0],[[-52,52],[142,-142]]);
 assert.deepEqual(E.GAMBLES[29],[[-256,256],[1260,-1260]]);
 assert.deepEqual(E.GAMBLES[12],[[-45,45],[-550,550]]);
 for(const pair of E.GAMBLES){assert.equal(pair.length,2);for(const outcomes of pair){assert.equal(outcomes.length,2);assert.equal(outcomes[0]+outcomes[1],0);}}
});
test('strict upper/lower absorption caps overshoots and remains absorbed',()=>{
 assert.deepEqual(E.applyBoundary(1850,300,'upper'),{rawWealth:2150,wealth:2000,absorbed:true});
 assert.deepEqual(E.applyBoundary(-1850,-300,'lower'),{rawWealth:-2150,wealth:-2000,absorbed:true});
 assert.equal(E.applyBoundary(1900,100,'upper').absorbed,false);
 assert.equal(E.applyBoundary(-1900,-100,'lower').absorbed,false);
 assert.equal(E.applyBoundary(2000,1,'upper').absorbed,true);
 assert.equal(E.applyBoundary(-2000,-1,'lower').absorbed,true);
 assert.equal(E.applyBoundary(2000,-500,'upper',true).wealth,2000);
 assert.equal(E.applyBoundary(-2000,500,'lower',true).wealth,-2000);
});
test('only the assigned boundary applies; unbounded wealth is never clamped',()=>{
 assert.equal(E.applyBoundary(0,-5000,'upper').wealth,-5000);
 assert.equal(E.applyBoundary(0,5000,'lower').wealth,5000);
 for(const v of [-8000,8000]) assert.deepEqual(E.applyBoundary(0,v,'none'),{rawWealth:v,wealth:v,absorbed:false});
});
test('choices resolve the displayed option; missing choice is worst of all four outcomes',()=>{
 const t={gambleId:1,sides:[1,0]};
 assert.equal(E.resolveTrial(0,t,0,'none',.1).outcome,142);
 assert.equal(E.resolveTrial(0,t,0,'none',.9).outcome,-142);
 assert.equal(E.resolveTrial(0,t,1,'none',.1).outcome,-52);
 const missed=E.resolveTrial(0,t,null,'none',.1);
 assert.equal(missed.outcome,-142);assert.equal(missed.selectedOption,null);assert.equal(missed.missed,true);
});
test('full schedule matches source ordering, randomized sides and session ordering',()=>{
 const orders=new Set();
 for(let seed=0;seed<100;seed++){
  const r=E.createRun('full',seed);assert.equal(r.order[0],'none');orders.add(r.order.join(','));assert.equal(r.practice.trials.length,8);
  for(const s of r.sessions){assert.equal(s.trials.length,30);assert.equal(new Set(s.trials.map(t=>t.gambleId)).size,30);assert.equal(s.wealth,0);if(s.condition!=='lower')assert.deepEqual(s.trials.map(t=>t.gambleId),Array.from({length:30},(_,i)=>i+1));for(const t of s.trials)assert.deepEqual([...t.sides].sort(),[0,1]);}
 }
 assert.equal(orders.size,2);
});
test('short modes use eight unique supplied pairs per condition',()=>{
 for(const mode of ['tour','demo']){const r=E.createRun(mode,123);for(const s of r.sessions){assert.equal(s.trials.length,8);assert.equal(new Set(s.trials.map(t=>t.gambleId)).size,8);}}
});
test('simulated full runs terminate correctly at crossings and produce auditable CSV',()=>{
 for(let seed=1;seed<=100;seed++){
  const r=E.createRun('full',seed),rnd=E.rng(seed+100);
  for(const s of r.sessions){for(const t of s.trials){const before=s.wealth,result=E.resolveTrial(before,t,1,s.condition,rnd());s.rows.push({...t,...result,events:[{side:1,atMs:230}],wealthBefore:before,startedAt:'2026-10-23T10:00:00Z',resolvedAt:'2026-10-23T10:00:03Z',interrupted:false});s.wealth=result.wealth;s.absorbed=result.absorbed;if(s.absorbed)break;}if(s.condition==='none')assert.equal(s.rows.length,30);if(s.absorbed)assert.equal(s.wealth,E.CONDITIONS[s.condition].boundary);}
  const csv=E.toCSV(r);assert.equal(csv.split('\r\n').length,1+r.sessions.reduce((a,s)=>a+s.rows.length,0));assert.match(csv,/first_choice_ms/);assert.match(csv,/selection_events/);
 }
});

test('learning follows the fixed Qualtrics signs for either option and either side',()=>{
 assert.deepEqual(E.PRACTICE_SIGNS,[1,-1,1,-1,-1,1,1,1]);
 for(let seed=0;seed<30;seed++){
  const run=E.createRun('full',seed);
  assert.equal(run.practice.outcomeMode,'scripted');
  for(let i=0;i<8;i++){
   const trial=run.practice.trials[i];
   for(const side of [0,1]){
    const result=E.resolvePractice(0,trial,side,i);
    assert.equal(Math.sign(result.outcome),E.PRACTICE_SIGNS[i]);
    assert.equal(Math.abs(result.outcome),Math.abs(E.GAMBLES[trial.gambleId-1][trial.sides[side]][0]));
    assert.equal(result.outcomeMode,'scripted');
    assert.equal(result.scriptStep,i+1);
    assert.deepEqual(result,E.resolvePractice(0,trial,side,i));
   }
  }
 }
 assert.throws(()=>E.resolvePractice(0,{gambleId:1,sides:[0,1]},null,0));
 assert.throws(()=>E.resolvePractice(0,{gambleId:1,sides:[0,1]},0,8));
});

test('scripted learning does not change the timed outcome resolution',()=>{
 const trial={gambleId:1,sides:[0,1]};
 assert.equal(E.resolvePractice(0,trial,0,0).outcome,52);
 assert.equal(E.resolveTrial(0,trial,0,'none',0).outcome,-52);
 assert.equal(E.resolveTrial(0,trial,0,'none',.5).outcome,52);
});

const choice=(option,extras={})=>({gambleId:1,selectedOption:option,selectedSide:1-option,missed:option===null,interrupted:false,...extras});
const session=(condition,rows,extras={})=>({condition,rows,trials:Array(30).fill({}),complete:true,absorbed:false,...extras});

test('diagnostic counts the higher-amplitude gamble, excludes misses, and compares percentages',()=>{
 const summaries=E.summarizeChoices([
  session('none',[choice(1),choice(0),choice(null),choice(null)]),
  session('lower',[choice(0),choice(0),choice(1),choice(0)],{absorbed:true}),
  session('upper',[choice(1),choice(1,{interrupted:true})])
 ]);
 assert.equal(summaries[0].riskyPercent,50);
 assert.equal(summaries[0].answered,2);
 assert.equal(summaries[0].missed,2);
 assert.equal(summaries[1].riskyPercent,25);
 assert.equal(summaries[1].differenceFromNoBoundary,-25);
 assert.equal(summaries[1].lowerRiskChoices,3);
 assert.equal(summaries[1].absorbed,true);
 assert.equal(summaries[2].riskyPercent,100);
 assert.equal(summaries[2].differenceFromNoBoundary,50);
 assert.equal(summaries[2].interrupted,1);
});

test('diagnostic has no percentage for unanswered or unplayed sessions',()=>{
 const summaries=E.summarizeChoices([
  session('none',[choice(null)]),session('upper',[]),session('lower',[choice(0)])
 ]);
 assert.equal(summaries[0].riskyPercent,null);
 assert.equal(summaries[1].riskyPercent,null);
 assert.equal(summaries[1].answered,0);
 assert.equal(summaries[2].riskyPercent,0);
 assert.equal(summaries[2].differenceFromNoBoundary,null);
 assert.ok(!JSON.stringify(summaries).includes('NaN'));
});

test('diagnostic excludes practice and retains correct denominator after early stopping',()=>{
 const run=E.createRun('full',25);
 run.practice.rows=Array(8).fill(choice(1));
 run.sessions[0].rows=[choice(1),choice(0),choice(0)];
 run.sessions[1].rows=[choice(1)];run.sessions[1].absorbed=true;
 const summaries=E.summarizeChoices(run.sessions);
 assert.equal(summaries[0].riskyChoices,1);
 assert.equal(summaries[0].riskyPercent,100/3);
 assert.equal(summaries[1].riskyPercent,100);
 assert.equal(summaries[1].played,1);
 assert.equal(summaries[2].riskyPercent,null);
});

test('restore preserves recorded legacy runs and upgrades only untouched learning',()=>{
 const untouched=E.createRun('full',1);untouched.version='1.0.0';delete untouched.practice.outcomeMode;
 assert.equal(E.restoreRun(untouched).practice.outcomeMode,'scripted');
 assert.equal(untouched.version,E.VERSION);
 const begun=E.createRun('full',1);begun.version='1.0.0';delete begun.practice.outcomeMode;
 begun.practice.rows=[{outcome:-52,wealth:-52}];
 assert.equal(E.restoreRun(begun).practice.outcomeMode,'random');
 assert.equal(begun.version,'1.0.0');
 assert.deepEqual(begun.practice.rows,[{outcome:-52,wealth:-52}]);
 assert.equal(E.restoreRun(null),null);
});

test('full bonus ranges are fixed by the offered gambles and the active boundary',()=>{
 const run=E.createRun('full',12);
 const ranges=Object.fromEntries(run.sessions.map(s=>[s.condition,E.bonusRange(s)]));
 assert.deepEqual(ranges.none,{min:-21053,max:21053});
 assert.deepEqual(ranges.upper,{min:-21053,max:2000});
 assert.deepEqual(ranges.lower,{min:-2000,max:21053});
 for(const s of run.sessions){
  const before=E.bonusRange(s);
  s.rows=[{gambleId:1,selectedOption:0}];s.wealth=200;s.absorbed=true;
  assert.deepEqual(E.bonusRange(s),before);
 }
});

test('hypothetical bonuses map endpoints to £0 and £3, are monotonic, and exclude practice',()=>{
 const run=E.createRun('full',8);
 run.practice.wealth=999999;
 for(const s of run.sessions){
  s.complete=true;
  const {min,max}=E.bonusRange(s);let last=-1;
  for(let step=0;step<=10;step++){
   s.wealth=min+(max-min)*step/10;
   const amount=E.summarizeBonus([s]).sessions[0].amountPence;
   assert.equal(amount,step*30);assert.ok(amount>=last);last=amount;
  }
 }
 assert.equal(E.summarizeBonus(run.sessions).totalPence,900);
 assert.equal(E.summarizeBonus(run.sessions).paid,false);
 assert.equal(run.bonusFraming,E.BONUS_RULE.id);
});

test('upper absorption yields £3 and lower absorption yields £0 using the full schedule',()=>{
 const run=E.createRun('full',9);
 for(const s of run.sessions){
  s.complete=true;
  s.wealth=s.condition==='none'?0:E.CONDITIONS[s.condition].boundary;
  s.absorbed=s.condition!=='none';
  s.rows=[{wealth:s.wealth}];
 }
 const bonus=E.summarizeBonus(run.sessions);
 assert.equal(bonus.totalPence,450);
 assert.equal(bonus.sessions.find(s=>s.condition==='upper').amountPence,300);
 assert.equal(bonus.sessions.find(s=>s.condition==='lower').amountPence,0);
});

test('short-mode ranges use the scheduled eight gambles; pending sessions have no bonus',()=>{
 for(const mode of ['tour','demo']){
  const run=E.createRun(mode,123),[first]=run.sessions;
  assert.deepEqual(E.bonusRange(first),{min:-5531,max:5531});
  assert.equal(E.summarizeBonus(run.sessions).totalPence,null);
  assert.ok(E.summarizeBonus(run.sessions).sessions.every(s=>s.amountPence===null));
  first.complete=true;first.wealth=0;
  assert.equal(E.summarizeBonus(run.sessions).sessions[0].amountPence,150);
  assert.equal(E.summarizeBonus(run.sessions).totalPence,null);
 }
});

test('bonus totals sum rounded pennies and previous runs do not acquire pre-play bonus framing',()=>{
 const run=E.createRun('full',4);
 for(const s of run.sessions){s.complete=true;s.wealth=1234;}
 const bonus=E.summarizeBonus(run.sessions);
 assert.equal(bonus.totalPence,491);
 assert.equal(bonus.totalPence,bonus.sessions.reduce((sum,s)=>sum+s.amountPence,0));
 run.version='1.1.0';delete run.bonusFraming;
 const restored=E.restoreRun(run);
 assert.equal(restored.version,'1.1.0');
 assert.equal(restored.bonusFraming,undefined);
 assert.equal(E.summarizeBonus(restored.sessions).totalPence,491);
});

test('scores above or below the range safely saturate the bonus in every mode and setting',()=>{
 for(const mode of ['full','tour','demo']){
  const run=E.createRun(mode,42);
  for(const s of run.sessions){
   s.complete=true;
   const {min,max}=E.bonusRange(s);
   for(const wealth of [max+1,1000000,Number.MAX_VALUE]){
    s.wealth=wealth;
    const result=E.summarizeBonus([s]).sessions[0];
    assert.equal(result.amountPence,300);
    assert.equal(result.finalPoints,wealth);
    assert.equal(s.wealth,wealth);
   }
   for(const wealth of [min-1,-1000000,-Number.MAX_VALUE]){
    s.wealth=wealth;
    assert.equal(E.summarizeBonus([s]).sessions[0].amountPence,0);
   }
  }
  for(const s of run.sessions)s.wealth=Number.MAX_VALUE;
  assert.equal(E.summarizeBonus(run.sessions).totalPence,900);
  for(const s of run.sessions)s.wealth=-Number.MAX_VALUE;
  assert.equal(E.summarizeBonus(run.sessions).totalPence,0);
 }
});

test('invalid scores and zero-width ranges do not yield misleading or non-finite bonuses',()=>{
 const run=E.createRun('full',1);
 for(const s of run.sessions)s.complete=true;
 for(const wealth of [NaN,Infinity,-Infinity,null,undefined,'1000']){
  run.sessions[0].wealth=wealth;
  const bonus=E.summarizeBonus(run.sessions);
  assert.equal(bonus.sessions[0].amountPence,null);
  assert.equal(bonus.totalPence,null);
 }
 run.sessions[0].wealth=0;
 run.sessions[0].trials=[];
 assert.equal(E.summarizeBonus(run.sessions).sessions[0].amountPence,null);
 assert.equal(E.summarizeBonus(run.sessions).totalPence,null);
});
