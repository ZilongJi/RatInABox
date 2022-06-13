# RatInABox 🐀📦

![](./readme_figs/whole_simulation.gif)

RatInABox is a toolkit for simulating navigation and/or hippocampal-entorhinal cell types. With it you can:

* Generate pseudo-realistic trajectories for rats exploring 1 and 2D environments
* Simulate spatially selective cells found in the Hippocampal-Entorhinal system (place cells, grid cells, boundary vector cells, and velocity cells). 

RatInABox represents a clean departure from pre-discretised "gridworld". Position and neuronal firing rates are calculated online with float precision. 

`RatInABox` contains three classes: 

1. `Environment()`: The environment/maze that the agent lives in. 1- or 2-dimensional.
2. `Agent()`: The agent (or "rat") moving around the Environment. 
3. `Neurons()`: A population of neurons with firing rates determined by the state of the Agent. 

The top animation shows the kind of simulation you can easily run using this toolbox. It shows an agent randomly exploring a 2D environment with a wall. Four populations of cells (place cells, grid cells, boundary vector cells and velocity cells) "fire" as the agent explores. Below shows the code needed to replicate this exact simulation using `RatInABox`(13 lines).

```
Env = Environment()
Ag = Agent(params={'Environment':Env})
PlaceCells = Neurons(params={'Agent':Ag,
                             'cell_class':'place_cell'})
GridCells = Neurons(params={'Agent':Ag,
                            'cell_class':'grid_cell'})
BoundaryVectorCells = Neurons(params={'Agent':Ag,
                                      'cell_class':'boundary_vector_cell'})
VelocityCells = Neurons(params={'Agent':Ag,
                                'cell_class':'velocity_cell'})

Env.add_wall(np.array([[0.3,0.0],[0.3,0.4]])) #add wall to Environment

while Ag.t < 60: #explore for 60 seconds
    Ag.update()
    PlaceCells.update()
    GridCells.update()
    BoundaryVectorCells.update()
    VelocityCells.update()
```

## Key features

* **Flexible**: Generate arbitrarily complex environments. 
* **Realistic**: Simulate large populations of neuronal cell types known to be found in the brain. 
* **Fast**: Simulating 1 minute exploration in a 2D environment with 100 place cells (dt=10 ms) take 2 seconds (but can be mush fast, e.g. in 1D mins on my laptop secs. 1 minutes exploration takes 3 seconds. Cells are rate based or Poisson spiking. 
* **Precise**: No more pre-discretised positions, tabular state spaces, or jerky movement policies. It's all continuous. 
* **Visual** It's easy plot or animate trajectories, firing rate timeseries', spike rasters, receptive fields, heat maps and more using our plotting functions. 
* **Easy**: sensible default parameters mean you can have realisitic simulation data to work with in ~10 lines of code. 

## Get started 
At the bottom of this readme we provide two scripts: one simple (10 lines of code to initialise and simulate and agnet in a 2D environment with 10 place cells) and one extensive (essentially the simulation animate at the top - a more complex environment with multiple cells types) which additionally demostrates how to use the plotting functions to visualise the data. 

## Requirements
* Python 3.7+
* NumPy
* Scipy
* Matplotlib
* Jupyter (optional)

## Installation 

## Feature run-down
Here is a list of features loosely organised into three categories: those pertaining to (i) the Environment, (ii) the Agent and (iii) the Neurons. 

### (i) `Environment()` features
#### Walls 
Arbitrarily add walls to the environment to replicate any desired maze structure using command:
```
Env.add_wall([[0.3,0.0],[0.3,0.5]])
```
Here are some easy to make examples.
![](./readme_figs/walls.png)

#### Boundary conditions 
Boundary conditions can be "periodic" or "solid". Place cells and the Agent will respect boundaries accordingly. 
```
Env = Environment(
    params = {'boundary_conditions':'periodic'} #or 'solid' (default)
) 
```
![](./readme_figs/boundary_conditions.png)

#### 1- or 2-dimensions 
Almost all features work in both 1 and 2 dimensions. The following figure shows 1 min of exploration of an agent in a 1D environment with periodic boundary conditions spanned by 10 place cells. 
```
Env = Environment(
    params = {'dimensionality':'1D'} #or '2D' (default)
) 
```
![](./readme_figs/one_dimension.png)


### (ii) `Agent()` features
#### Wall repelling 
Walls in the environment mildly "repel" the agent. Coupled with the finite turning speed this creates, somewhat counterintuitively, an effect where the agent is biased to over-explore near walls and corners (as shown in these heatmaps) matching real rodent behaviour. It can also be turned off.
```
Αg.walls_repel = True #False
```
![](./readme_figs/wall_repel.png)

#### Random motion model
Motion is stochastic but smooth. The speed (and rotational speed if in 2D) of an Agent take constrained random walks governed by Ornstein-Uhlenbeck processes. You can change the variance and coherence times of these processes to control the shape of the trajectory.

```python
Agent.speed_mean = 0.2
Agent.speed_std = 0.1
Agent.speed_coherence_time = 3
Agent.rotation_velocity_std = 0.1
Agent.rotational_velocity_coherence_time = 3
```
The following set of trajectories were generated by modifying the rotational_velocity_std
![](./readme_figs/motion_model.png)


#### Policy control 
By default the movement policy is an uncontrolled (e.g. displayed above). It is possible, however, to manually pass a "drift_velocity" to the Agent on each `update()` step. The agent velocity will drift towards drift velocity. We envisage this being use, for example, by an Actor-Critic system to control the Agent. The actor-critic system could take as input the firing rate of some Neurons(). As a demonstartion that this method can be used to control the agent's movement here we set a radial drift velocity to encourage circular motion.   
```
Agent.update(drift_velocity=drift_velocity)
```
![](./readme_figs/policy_control.png)


### (iii) `Neuron()` features 

#### Multiple cell types: 
Currently supported cell types (`params['cell_class']`)  are: 
* `"place_cells"`
* `"grid_cells"`: rectified sum of three cosine plane waves
* `"boundary_vector_cells"`: double exponential model matching de Cothi and Barry (2020)
* `"velocity_cells"`: cells encode positive and negative x and y velocitys (2N cells in N-dimensions)

Place cells come in multiple types (give by `params['description']`):
* `"gaussian"`: normal gaussian place cell 
* `"gaussian_threshold"`: gaussian thresholded at 1 sigma
* `"diff_of_gaussian"`: gaussian(sigma) - gaussian(1.5 sigma)
* `"top_hat"`: circular receptive field, max firing rate within, min firing rate otherwise
* `"one_hot"`: the closest palce cell to any given location is established. This and only this cell fires. 

This last place cell type, `"one_hot"` is prticularly useful as it essentially rediscretises space and tabularises the state space (gridworld again). This can be used to effortlessly contrast and compare learning algorithms acting over continuous vs discrete state spaces. 

#### Geometry
Choose how you want place cells to interact with walls in the environment. We provide three types of geometries. 
![](./readme_figs/wall_geometry.png)

#### Spiking 
All neurons are rate based. Concurrently spikes are sampled at each time step as though neurons were Poisson neurons. These are stored in `Neurons.history['spikes']`. The max and min firing rates can be set with `Neurons.max_fr` and  `Neurons.min_fr`.
```
Neurons.plot_rate_timeseries(spikes=True)
Neurons.plot_ratemap(spikes=True)
```
![](./readme_figs/spikes.png)


#### Rate maps 
Place cells, grid cells and boundary vector cells have analytic receptive fields. These can be displayed by querying their firing rate at an array of positions spanning the environment, then plotting. 

An alternative, and ultimately more robust way to display the receptive field is to plot a heatmap of the positions of the Agent has visited where each positions contribution to a bin is weighted by the firing rate observed at that position. Over time, as coverage become complete, the firing fields become visible.  Velocity neurons provide an interesting  example; they have no predefined/analytic "receptive field" but the firing-rate-weighted position heatmap is still well defined and can be plotted. The velocity neuron shown (v_x^+) is most active near the north and south boundaries where the agent rushes along. 
```
Neurons.plot_rate_map() #attempted to plot analytic rate map 
Neurons.plot_rate_map(by_history=True) #plots rate map by firing-rate-weighted position heatmap
``` 
![](./readme_figs/rate_map.png)

#### More complex Neuron types
We encourage more complex Neuron classes to be made with the Neuron() class as parent. Specifically by writing your own `update()` and `get_state()` you can create more complex neuron types. For example  you could write a Neuron() class to fire as a weighted sum inputs from another neuronal layers (for example George and de Cothi et al. (2022)). Or maybe implement a recurrent layer feeding into itself. By saving `firingrate` at each step plotting functions shown here should still be functional for downstream analysis.

## Tutorial 
A tutorial script can be found in scripts/ratinabox_tutorial.ipynb. This outlines most of the functionality. Nb. I haven't writen this yet. 

## Contribute 
RatInABox is an open source project, and we actively encourage community contributions. These can take various forms, such as new movement policies, new cells types, new geometries, bug fixes, documentation, citations of relevant work, or additional experiment notebooks. If there is a small contribution you would like to make, please feel free to open a pull request, and we can review it. If there is a larger contribution you are considering, please open a github issue. This way, the contribution can be discussed, and potential support can be provided if needed. 

## Example Scripts



