from gym_duckietown.tasks.task_solution import TaskSolution
import numpy as np
import cv2

class DontCrushDuckieTaskSolution(TaskSolution):
    def __init__(self, generated_task):
        super().__init__(generated_task)

    def solve(self):
        env = self.generated_task['env']
        # getting the initial picture
        obs, _, _, _ = env.step([0,0])
        # convect in for work with cv
        img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB)

        condition = True
        while condition:
            obs, reward, done, info = env.step([1, 0])
            img = cv2.cvtColor(np.ascontiguousarray(obs), cv2.COLOR_BGR2RGB)

            #lower and upper range of yellow in RGB
            yellowLower = np.array([0,135,155])
            yellowUpper = np.array([10,255,255])

            yellowMask = cv2.inRange(img, yellowLower, yellowUpper) #yellow mask

            nonzeroPixels = cv2.findNonZero(yellowMask) # we get non zero pixels

            if nonzeroPixels is not None: #if there is a non zero pixel
                nonzeroPixelsLength = len(nonzeroPixels)
                if (nonzeroPixelsLength / img.size) > 0.01:  #if it's close enough we stop the car
                    obs, reward, done, info = env.step([0, 0]) # stop car
                    condition = False

            env.render()
