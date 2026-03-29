https://blog.block.science/how-to-perform-parameter-selection-under-uncertainty/


Exploring tradeoffs between various system goals requires data and visualizations to make discoveries actionable for stakeholders.
— BlockScience, cadCAD, Uncertainty, Parameterization, Systems Engineering —
How to Perform Parameter Selection Under Uncertainty
April 08, 2021
Configuring Complex Systems to Handle the Real World
This article aims to educate the reader on the concept of parameter selection under uncertainty — in other words, how we configure complex ecosystems in situations when we don’t have perfect information. This methodology is a workflow for scientifically iterating multi-dimensional, multi-stakeholder systems with the goal of making actionable recommendations in regards to parameter selection. Through the clear definition system goals and parameters, we perform a variety of tests that can inform the most important aspects of the system under different circumstances, ensuring more robust and reliable system design.


Real world deployments are fraught with complex decisions and imperfect information. How to navigate these deployments safely, using replicable engineering processes is the topic of this article.
Introduction, Motivation and Context
In any dynamical complex system, values of system parameters play a crucial role as they influence the magnitude of environmental events, user actions as well as control mechanisms, and therefore determine the evolution of the system. Their initial selection and maintenance over time are important governance decisions which lie in the responsibility of system stakeholders that will define the initial conditions and the trajectory of the system. Therefore these tasks are particularly important in the engineering process of digital ecosystems — for example in cryptoeconomies.

System parameters are deducted through a procedure that is supported by computational modeling and simulation methods which are themselves embedded into the more general design flow of the engineering process. The decisive role is fulfilled by quantifiable metrics derived from qualitative system goals driven by business objectives and implementation decisions.

These metrics will inform parameter choices as they will pin down the trade-offs of particular realizations of different system configurations. Knowing and understanding the importance of the process and subsequently collaborating in its application gives stakeholders the opportunity to not only contribute to design decisions on the performance of the system, but also in its broader economic context.

The purpose of this article is to educate the reader about the process of Parameter Selection Under Uncertainty (PSuU) and explain how it is embedded into the wider system engineering design workflow.


Parameter selection can have wide-ranging and unintuitive effects in cryptoeconomic systems involving large amounts of agent interactions, so the process must be scientific and data-driven.
Parameter Selection Process Overview
The PSuU workflow consists of first identifying, naming and defining the system goals. This enables the definition of how to measure them appropriately, with explicit indicators and metrics, and finally sets the stage for deriving optimal values from that. This helps to filter our important system parameters based on requirements and attach quantifiable indicators to them. The typical process is composed of the following steps which might depend on the specific project and use case:

1. System goals identification

2. Control parameter identification

3. Environmental parameter identification

4. Metric identification

5. Simulation

6. Optimal parameter selection
Metrics could be obvious and straight forward in some cases (e.g. maximization of profit) but other scenarios call for more sophisticated or tailored solutions to reflect the particularities of a more complex system or capture unintuitive relations.

Trade-offs have to be considered if some of the system goals get in the way or contradict each other. It might also happen that full goal achievements are infeasible due to costly, impractical deployments — in that case, graduated goal setting can be applied, with trade-offs balanced as needed.

Involving system stakeholders helps to figure out the main focus of the project, how they are perceiving the outcome and in which direction it should continue.

Embeddedness in the Engineering Process
The parameter selection process is only a part of the general engineering process flow. Several prerequisites have to be met for this process to be possible:

System requirements have been specified fully
The mathematical specification has been created
The computational model has been programmed
With these instruments at hand the stage is set for understanding how optimal parameters can be selected.

Parameter Selection Under Uncertainty in Detail
Step 1: System Goals Identification
This steps connects the qualitative definitions of targets articulated by the team to concrete and precise system goals. It helps to attach quantitative measures to the qualitative statements. It is key to ensure that simulation parameters and metrics are aligned with the overall objective.

Step 2: Control Parameters Identification
In this step, parameters are identified that are under control by the system, and impact the outcome of system goals. They can be proposed by the project team — if there is an idea what the controller is (e.g. fee rate, minting rate) — with the intention to set the ideal parameter. More generally either controllers can be unspecified or their impact might be unknown.

A key point is that trade-offs between system goals will occur and the more complex the system the more difficult it is to optimize for all goals. However there are ranges of parameters that will favor some goals simultaneously to a different extent. Therefore a parameter-goal impact assessment is advisable to allow stakeholders to make a prioritization of the system goals when impacts and consequences are sufficiently understood. This can be compared with the simulation results to arrive at a ranking of various parameter selections.


Dynamic system goals can be balanced through feedback (both positive or negative) from embedded controller mechanisms.
Step 3: Environmental Parameters Identification
In this step all processes are recorded that cannot be controlled but are important so far as they do affect the system goals. Those systemic events and their effects can then be targeted by available control mechanisms even if they are taken as variable from the environment. For example, the price of ETH may factor into a model, but it is not under control of the model.

Step 4: Metrics Definition
In this step qualitative goals are translated into quantifiable metrics as closely as possible. System goals and metrics are not exclusive — there might be more KPIs for one system goal or conversely several system goals might share the same metrics.

Metrics can be of different types as they can measure different system characteristics e.g. stability, liquidity, responsiveness. In any case, metrics allow to not only optimize for system targets but also help to identify thresholds beyond which the system is unresponsive or unstable.

In the subsequent selection process, the control parameters are selected given the realizations of the environmental parameters such that defined metrics are fulfilled. This makes the metrics to be the criteria by which the control parameters are chosen.


Exploring tradeoffs between various system goals requires data and visualizations to make discoveries actionable for stakeholders.
Step 5: Simulation
In this step scenarios are defined that are to be tested against the system goals. All uncontrolled environmental parameters are represented by generated processes. For controllable parameters, ranges for value sweeps are defined so that simulation experiments can be performed in multiple runs.

Afterwards, the robustness of the parameters and their impacts on the system are tested through a sensitivity analysis.

Step 6: Optimal Parameter Selection
The optimal values can be selected by assessment of the previously stated metrics. Based on basins of attraction and confidence intervals, choice recommendations can be done. A ranking allows to order optimal parameters according to the prioritized list of system goals.


A demonstration of a basin of attraction, where initial conditions end up ‘attracted’ to the desired final state of the system. (source)
Practical Considerations and Challenges
The knowledge of the process itself and deep understanding of its use are key factors in its successful application. Being aware of the current position in this process and what the work focuses on gives the biggest benefits to the project team. Everything depends on understanding of all work items that were done before — such as requirement definition, modeling and specification, mathematical specification — as they all set the stage how to articulate the metrics in the context of the system goals.

This process serves as a framework to proceed iteratively from an initial point of departure without reinventing the wheel, while improving the understanding of the system with each step. In this way it allows to change the perspective and reorder goal priorities when additional insights require adaptations. In addition it makes sure that through the rigorous initial definition of system goals subsequent work is anchored to those definitions and hypotheses, which allows for consistent scientific progress.

Applied correctly, this process supports and preserves a narrative flow of the system creators by making their intuition about parameter dependencies more tangible and ultimately helping them to find an area near the optimal parameter values that supports the envisaged system goals considering all important trade-offs.

Article by

Krzysztof Paruch and Jamsheed Shorish, with edits and suggestions by Michael Zargham, Danilo Lessa Bernardineli, Jeff Emmett, and Jessica Zartler.

About BlockScience
BlockScience® is a complex systems engineering, R&D, and analytics firm. Our goal is to combine academic-grade research with advanced mathematical and computational engineering to design safe and resilient socio-technical systems. We provide engineering, design, and analytics services to a wide range of clients, including for-profit, non-profit, academic, and government organizations, and contribute to open-source research and software development.