# Simulated Multisensory Integration
This project is the Phase 1 part of the whole Bodily-Self Spiking Neural Computational Model. The goal of this project is to provide a relatively simple and neat environment for the theory exploration. After the exploration, the model will be moved to the real-world robot platform, controlling the real NAO and iCub robots to own bodily-self model.
  
The project contains two functional modules: dopamine-based reinforcement learning, and multisensory integration. The engineering plan of the project is listed below. 

| Functional Module | Goal | Expected Time | Purpose | Content | Output|
| :----| :---- | :---- |:----| :---- |:----|
| Dopamine-based RL | Dopamine-based RL on 2-DoF simplified arm | 1.5 weeks | 1. Build the control model<br> 2. Provide postion notion for self model | 1. Implement the SNN control model <br>2. Learn Brian2 | 1.Prioproception layer<br>2. Motor layer <br>3. Position coding for vision  |
| Multisensory Integration | Target reaching driven multisensory integration | 2 weeks | 1.Implement multisensory integration part<br> 2.Encode postion | 1.Gather the postion, visual, angle data <br>2.Train the visual network. <br>3.Train the integration SNN| 1.Position encoding layer<br> 2.Multisensory integration layer  |
| Naive bodily self identification model for NAO robot | Target reaching driven multisensory integration on NAO | 2 weeks | 1.Test model on real world robotics platfor<br> 2.Enhance and revise the NN ability for complex visual input | 1.Learn to get the Cartesian position, visual, angle data of NAO robot end effector<br>2.Labeling the data for later classfication task.<br>3.Attention model or CNN model for foreground extraction<br> 4. Train the classification model for prioproception and vision<br> 5. Train the integration model| 1.A real world self identification model for NAO robot |
