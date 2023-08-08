# Welcome to EE_web_apps

## Introduction

Welcome to the EE_web_apps repository, where we delve into the realm of Ergodicity Economics (EE). In EE, our aim is to elucidate the intricacies of human decision-making processes and economic behaviors through a rigorous mathematical framework. Our fundamental inquiry revolves around a crucial question: Do the governing dynamics of a system depend on time, and are they ergodic?

To grasp the depth of these concepts and explore some remarkable findings, we invite you to visit the [Ergodicity Economics webpage](https://ergodicityeconomics.com/). Further insights can be found in the pioneering publication "The Ergodicity Problem in Economics" by Peters, Peters, and O. in *Nature Physics* (Volume 15, Pages 1216–1221, 2019), available at [DOI: 10.1038/s41567-019-0732-0](https://doi.org/10.1038/s41567-019-0732-0).

## Simulations and Exploration

Within this repository, we present a collection of simulations designed to illuminate key economic concepts and applied ergodicity principles. These simulations are powered by Streamlit and implemented using Python scripts. You can experience them firsthand on the Ergodicity Economics blog. Additionally, we offer the flexibility to engage with these simulations locally by following the installation instructions provided below.

We're excited to guide you through this intriguing journey into the intersection of economics and ergodicity.


## dependencies
### About the Simulations

The simulations are written in Python code and are executed using Streamlit. To fully understand and interact with these simulations on GitHub, it's recommended to familiarize yourself with Streamlit by exploring their homepage and documentation.

To run the simulations locally, you'll need to ensure you have both Python and Streamlit properly installed. Below, we offer guidance on installing Streamlit, especially in combination with Anaconda. Note that this is just one of the options available for running the simulations, so feel free to choose the method that suits you best.

### Anaconda
Anaconda is a software distribution that provides a convenient way to run Python code. It includes Python and various libraries commonly used for scientific computing, data analysis, and machine learning. Anaconda simplifies setting up and managing these libraries, making it easier for users to work with Python-based projects without worrying about compatibility issues or complex installations. It's especially useful for projects that require specific versions of libraries or need to be isolated from each other to prevent conflicts.

Installation of anaconda and primary usage documentation can be found on the anaconda installation manual and homepage, listed below in the links section.

### Streamlit

Streamlit is a Python library that enables the creation of interactive web applications directly from Python scripts. It's designed to simplify the process of turning data scripts into shareable web apps, allowing users to visualize data, run simulations, or build simple interfaces without the need for web development expertise. With Streamlit, developers can focus on their data analysis or modeling tasks and easily transform their work into interactive applications that users can access through a web browser. This makes it a valuable tool for quickly prototyping and sharing data-driven applications and insights.

Installation and documentation can be found on the streamlit homepage, as listed in the links section.

## Setting Up a new Environment

To ensure a clean environment for running the Streamlit simulations, follow these steps:

1. **Create a Clean Conda Environment:**

   Open your command line interface and execute the following command to create a new environment named `env-streamlit-test` with Python version 3.11:

  'conda create --name env-streamlit-test python=3.11'
  
This will set up a fresh Python environment based on the version you specify.

2. **Activate the Environment:**

Activate the newly created environment to prepare it for Streamlit installation:

  'conda activate env-streamlit-test'

3. **Install Streamlit:**

Within the activated environment, install Streamlit using the following command:

  'conda install streamlit'

This command will install Streamlit and its dependencies in the environment.

4. **Test Streamlit Installation:**

Verify that Streamlit is installed correctly by running a test command:

  'streamlit hello'

If Streamlit is properly installed, this command should start a local server and display a "Hello!" message in your web browser.

Now you have a clean environment with Streamlit installed, ready to run the simulations on your local machine. For further instructions on running specific simulations, refer to the Streamlit documentation.

### Example Coin-Toss experiment:
That's it, you're now ready to start the simulations on your local machine.
How to do this is described in the aforementioned documentation of streamlit but basically the steps are easy.
You download the simulation you want to run as a python script to your local machine.
Store the script in your new environment's directory and enter in the commandline:

streamlit run 'cointoss_basicinput.py'

## Links
[Ergodicity Economics webpage](https://ergodicityeconomics.com/)
[Initial Nature publication](https://doi.org/10.1038/s41567-019-0732-0)
[Anaconda installation manual](https://docs.anaconda.com/free/anaconda/install/index.html)
[Streamlit homepage](https://streamlit.io/)
[Streamlit installation guide](https://docs.streamlit.io/library/get-started/installation)
[Streamlit documentation](https://docs.streamlit.io/)
