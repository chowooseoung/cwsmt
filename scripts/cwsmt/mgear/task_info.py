# -*- coding:utf-8 -*-

# mgear
import mgear.shifter.custom_step as cstp

# maya
import pymel.core as pm

# 
import json
import sys
import os


class CustomShifterStep(cstp.customShifterMainStep):
    def __init__(self):
        self.name = "task_info"


    def run(self, stepDict):
        """Run method.

            i.e:  stepDict["mgearRun"].global_ctl  gets the global_ctl from
                    shifter rig build bas
            i.e:  stepDict["mgearRun"].components["control_C0"].ctl  gets the
                    ctl from shifter component called control_C0
            i.e:  stepDict["otherCustomStepName"].ctlMesh  gets the ctlMesh
                    from a previous custom step called "otherCustomStepName"
        Arguments:
            stepDict (dict): Dictionary containing the objects from
                the previous steps

        Returns:
            None: None
        """
        self.task = None
        self.get_task()

        if self.task:
            sys.stdout.write("### task ###\n\n")
            for key, value in self.task.items():
                sys.stdout.write("{key} : {value}\n".format(key=key, value=value))
            sys.stdout.write("\n### task end ###\n")
        else:
            sys.stdout.write("### None task ###")
        return

    def get_task(self):
        scene = pm.system.sceneName()
        workdir = scene.parent.parent
        taskdir = workdir / "taskdir" / scene.basename().namebase
        task_json = taskdir / "task.json"

        if os.path.exists(task_json):
            with open(task_json, "r") as f:
                self.task = json.load(f)
        


