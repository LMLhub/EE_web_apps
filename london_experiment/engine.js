(function (root) {
  'use strict';
  const VERSION = '1.2.0';
  const BONUS_RULE = {id:'theoretical-range-v1',currency:'GBP',maxPencePerSession:300,paid:false,rangeBasis:'app-defined theoretical extrema of the scheduled gambles, limited only by the active boundary'};
  // QID837–841 and QID857–859 in the active Qualtrics training loop.
  // Keep this app's practice amounts, but reproduce the source win/loss sequence.
  const PRACTICE_SIGNS = [1,-1,1,-1,-1,1,1,1];
  const GAMBLES = [
    [[-52,52],[142,-142]], [[161,-161],[-251,251]], [[-237,237],[327,-327]],
    [[-55,55],[259,-259]], [[156,-156],[360,-360]], [[-257,257],[461,-461]],
    [[-38,38],[331,-331]], [[146,-146],[-439,439]], [[251,-251],[544,-544]],
    [[-49,49],[457,-457]], [[-140,140],[-548,548]], [[246,-246],[-654,654]],
    [[-45,45],[-550,550]], [[142,-142],[647,-647]], [[-248,248],[753,-753]],
    [[37,-37],[643,-643]], [[-149,149],[755,-755]], [[261,-261],[-867,867]],
    [[60,-60],[765,-765]], [[-140,140],[-845,845]], [[260,-260],[965,-965]],
    [[-36,36],[844,-844]], [[139,-139],[-947,947]], [[-245,245],[1053,-1053]],
    [[-46,46],[-955,955]], [[136,-136],[1045,-1045]], [[256,-256],[-1165,1165]],
    [[48,-48],[1052,-1052]], [[-165,165],[1169,-1169]], [[-256,256],[1260,-1260]]
  ];
  const CONDITIONS = {
    none: {name:'No boundary', short:'Unbounded', boundary:null, color:'#003558', description:'Your points can rise or fall without a limit.'},
    upper: {name:'Upper boundary', short:'Upper boundary', boundary:2000, color:'#b78e3b', description:'If your wealth goes above +2,000, this session ends. Your final wealth is recorded as +2,000.'},
    lower: {name:'Lower boundary', short:'Lower boundary', boundary:-2000, color:'#647993', description:'If your wealth goes below −2,000, this session ends. Your final wealth is recorded as −2,000.'}
  };
  function rng(seed) { let a=seed>>>0; return () => { a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
  function shuffle(items, random) { const a=[...items]; for(let i=a.length-1;i>0;i--) { const j=Math.floor(random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
  function applyBoundary(wealth, outcome, condition, alreadyAbsorbed=false) {
    const boundary=CONDITIONS[condition].boundary;
    if(alreadyAbsorbed) return {rawWealth:wealth,wealth:boundary,absorbed:true};
    const rawWealth=wealth+outcome;
    const absorbed=(condition==='upper' && rawWealth>2000)||(condition==='lower' && rawWealth< -2000);
    return {rawWealth,wealth:absorbed?boundary:rawWealth,absorbed};
  }
  function resolveTrial(wealth, trial, side, condition, outcomeDraw) {
    if(side!==null && side!==0 && side!==1) throw new Error('Invalid choice');
    const missed=side===null;
    const option=missed?null:trial.sides[side];
    const pair=GAMBLES[trial.gambleId-1];
    const outcomeIndex=missed?null:(outcomeDraw<0.5?0:1);
    const outcome=missed?Math.min(...pair.flat()):pair[option][outcomeIndex];
    return {selectedSide:side, selectedOption:option, missed, outcomeIndex, outcome, ...applyBoundary(wealth,outcome,condition)};
  }
  function resolvePractice(wealth, trial, side, step) {
    if(side!==0 && side!==1) throw new Error('Practice requires a choice');
    if(!Number.isInteger(step) || step<0 || step>=PRACTICE_SIGNS.length) throw new Error('Invalid practice step');
    const outcomes=GAMBLES[trial.gambleId-1][trial.sides[side]];
    const outcomeIndex=outcomes.findIndex(value=>Math.sign(value)===PRACTICE_SIGNS[step]);
    return {...resolveTrial(wealth,trial,side,'none',outcomeIndex===0?0:0.5),outcomeMode:'scripted',scriptStep:step+1};
  }
  function summarizeChoices(sessions) {
    const summaries=sessions.map(session=>{
      const answered=session.rows.filter(row=>!row.missed && (row.selectedOption===0 || row.selectedOption===1));
      const risky=answered.filter(row=>{
        const amplitudes=GAMBLES[row.gambleId-1].map(option=>Math.max(...option.map(Math.abs)));
        return amplitudes[row.selectedOption]>amplitudes[1-row.selectedOption];
      }).length;
      return {
        condition:session.condition, played:session.rows.length, answered:answered.length,
        missed:session.rows.filter(row=>row.missed).length,
        interrupted:session.rows.filter(row=>row.interrupted).length,
        riskyChoices:risky, lowerRiskChoices:answered.length-risky,
        riskyPercent:answered.length?100*risky/answered.length:null,
        complete:session.complete, absorbed:session.absorbed
      };
    });
    const baseline=summaries.find(summary=>summary.condition==='none')?.riskyPercent;
    return summaries.map(summary=>({...summary,differenceFromNoBoundary:
      baseline!=null && summary.riskyPercent!=null?summary.riskyPercent-baseline:null}));
  }
  function bonusRange(session) {
    // Use the whole schedule, including unplayed trials after absorption.
    // The range depends on the offered gambles, never on choices or observed scores.
    const span=session.trials.reduce((total,trial)=>total+Math.max(...GAMBLES[trial.gambleId-1].flat().map(Math.abs)),0);
    return {min:session.condition==='lower'?Math.max(-span,CONDITIONS.lower.boundary):-span,
      max:session.condition==='upper'?Math.min(span,CONDITIONS.upper.boundary):span};
  }
  function summarizeBonus(sessions) {
    const amounts=sessions.map(session=>{
      const range=bonusRange(session);
      const complete=Boolean(session.complete);
      const valid=Number.isFinite(session.wealth) && Number.isFinite(range.min) && Number.isFinite(range.max) && range.max>range.min;
      // Clamp before arithmetic so even extreme finite scores cannot overflow the conversion.
      // Preserve the actual score in the result; only the bonus uses the bounded value.
      const boundedPoints=valid?Math.max(range.min,Math.min(range.max,session.wealth)):null;
      const fraction=valid?(boundedPoints-range.min)/(range.max-range.min):null;
      const amountPence=complete && Number.isFinite(fraction)?Math.round(BONUS_RULE.maxPencePerSession*Math.max(0,Math.min(1,fraction))):null;
      return {condition:session.condition,...range,finalPoints:complete?session.wealth:null,complete,amountPence};
    });
    return {...BONUS_RULE,sessions:amounts,totalPence:amounts.length===3 && amounts.every(s=>s.amountPence!==null)?amounts.reduce((total,s)=>total+s.amountPence,0):null};
  }
  function restoreRun(saved) {
    if(!saved || ![VERSION,'1.1.0','1.0.0'].includes(saved.version) || saved.sessions?.length!==3 || !saved.practice) return null;
    // Preserve completed observations and the original practice protocol of an ongoing run.
    // A run with no recorded decisions can safely adopt the new learning protocol.
    if(!saved.practice.outcomeMode) {
      const untouched=saved.practice.rows.length===0 && saved.sessions.every(session=>session.rows.length===0) && !saved.activeTrial;
      saved.practice.outcomeMode=untouched?'scripted':'random';
      if(untouched) saved.version=VERSION;
    }
    return saved;
  }
  function makeSession(condition, mode, random) {
    const indices=Array.from({length:30},(_,i)=>i+1);
    let order=condition==='lower'?shuffle(indices,random):indices;
    // Short modes sample across the full range without changing the gambles.
    if(mode!=='full') order=condition==='lower'?order.slice(0,8):[1,5,9,13,17,21,25,30];
    return {condition, trials:order.map(gambleId=>({gambleId,sides:random()<0.5?[0,1]:[1,0]})), rows:[], wealth:0, absorbed:false, complete:false};
  }
  function createRun(mode,seed) {
    const random=rng(seed), order=['none',...shuffle(['upper','lower'],random)];
    return {version:VERSION,bonusFraming:BONUS_RULE.id,id:`boundary-${Date.now().toString(36)}-${seed.toString(16)}`,seed,mode,startedAt:new Date().toISOString(),status:'active',stage:mode==='demo'?'intro':'instructions',sessionIndex:0,order,sessions:order.map(c=>makeSession(c,mode,random)),practice:{outcomeMode:'scripted',trials:[1,4,8,12,16,20,24,30].slice(0,mode==='full'?8:3).map(gambleId=>({gambleId,sides:random()<0.5?[0,1]:[1,0]})),rows:[],wealth:0},checks:[],attempts:{},activeTrial:null};
  }
  const csvFields=['run_id','version','mode','seed','session','condition','trial','gamble_id','left_option','right_option','left_outcome_1','left_outcome_2','right_outcome_1','right_outcome_2','selected_side','selected_option','missed','first_choice_ms','last_choice_ms','choice_count','outcome_index','outcome','wealth_before','raw_wealth','wealth_after','absorbed','interrupted','started_at','resolved_at','selection_events'];
  function csvEscape(v) { const s=v===null||v===undefined?'':String(v); return /[",\r\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s; }
  function toCSV(run) {
    const rows=run.sessions.flatMap((s,i)=>s.rows.map((r,j)=>{
      const pair=GAMBLES[r.gambleId-1],left=pair[r.sides[0]],right=pair[r.sides[1]];
      return [run.id,run.version,run.mode,run.seed,i+1,s.condition,j+1,r.gambleId,r.sides[0]+1,r.sides[1]+1,...left,...right,r.selectedSide===null?'':r.selectedSide===0?'left':'right',r.selectedOption===null?'':r.selectedOption+1,r.missed,r.events[0]?.atMs,r.events.at(-1)?.atMs,r.events.length,r.outcomeIndex===null?'':r.outcomeIndex+1,r.outcome,r.wealthBefore,r.rawWealth,r.wealth,r.absorbed,r.interrupted,r.startedAt,r.resolvedAt,JSON.stringify(r.events)];
    }));
    return [csvFields,...rows].map(row=>row.map(csvEscape).join(',')).join('\r\n');
  }
  const api={VERSION,BONUS_RULE,GAMBLES,CONDITIONS,PRACTICE_SIGNS,bonusRange,summarizeBonus,rng,shuffle,applyBoundary,resolveTrial,resolvePractice,summarizeChoices,restoreRun,createRun,toCSV};
  if(typeof module!=='undefined'&&module.exports) module.exports=api; else root.BoundaryEngine=api;
})(typeof globalThis!=='undefined'?globalThis:this);
