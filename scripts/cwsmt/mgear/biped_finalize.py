
# -*- coding:utf-8 -*-

# mgear 
import mgear.shifter.custom_step as cstp
import mgear.core.skin as skin

# maya
import pymel.core as pm


class CustomShifterStep(cstp.customShifterMainStep):
    def __init__(self):
        self.name = "biped_finalize"

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
        self.step_dict = stepDict
        self.model_name = stepDict["mgearRun"].model.name()

        self.controllers_grp = pm.PyNode("{0}_controllers_grp".format(self.model_name))
        self.deformers_grp = pm.PyNode("{0}deformers_grp".format(self.model_name))
        self.editing_custom_biped()

        return

    def editing_custom_biped(self):
        self.controllers_grp.renmae("controller_SET")
        self.deformers_grp.renmae("skinjoint_SET")

    def edit_sets(self):
        pass

    def import_skin(self):
        pass

    def import_geo(self):
        pass


