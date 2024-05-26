import shap
import pandas as pd
import matplotlib.pyplot as plt
from test import get_model_x
import os

shap.initjs()

class ShapeExplainPlotter:
    def __init__(self, model, training_set, out_model_name, path_to_save=None):
        self.model = model
        self.explainer = shap.Explainer(self.model)
        self.training_set = training_set
        self.shap_values = None
        self.path_to_save = path_to_save
        self.out_model_name = out_model_name
        self.plot_mapping = {
            "waterfall": self.plot_waterfall,
            "force": self._plot_force,
            "bar" : self._plot_bar,
            "bees" : self._plot_bees,
            "scatter": self._plot_scatter,
        }


    def compile(self, show_plot=True, save_plots=True, plot_list=None,
                max_features=10, idx_row_focus=0, feature_name = None,scatter_color_by_feature = None,force_kwargs={},
                bees_kwargs = {},scatter_kwargs = {}):
        
        if not isinstance(self.training_set, pd.DataFrame):
            raise ValueError("Training set must be a DataFrame with valid feature names")

        if not plot_list:
            plot_list = ["waterfall","force","bar","bees","scatter"]

        self.shap_values = self.explainer(self.training_set)

        if save_plots:
            if not self.path_to_save:
                raise MemoryError("Saving Plots requires a path to save plots")
            else:
                self.path_to_save = os.path.join(self.path_to_save, self.out_model_name)

        for plot_name in plot_list:
            if plot_name not in self.plot_mapping:
                raise ValueError(f"Plot name {plot_name} is not a valid plot name")

            fig_axis = self.plot_mapping[plot_name](
                self.shap_values[idx_row_focus],
                feature_name = feature_name,
                max_display = max_features,
                complete_shap_values = self.shap_values,
                scatter_color_by_feature = scatter_color_by_feature,
                force_kwargs=force_kwargs,
                bees_kwargs=bees_kwargs,
                scatter_kwargs = scatter_kwargs
            )

            if save_plots:
                figure = fig_axis.figure
                figure.savefig(self.path_to_save + "_" + plot_name, dpi=300, bbox_inches="tight")

            if show_plot:
                plt.show()

            plt.close(figure)

    def plot_waterfall(self, shape_values, max_display, *args, **kwargs):
        fig_axis = shap.plots.waterfall(
            shape_values, max_display=max_display, show=False
        )
        return fig_axis
    
    def _plot_force(self, shape_values, *args, **kwargs):
        force_kwargs = kwargs.get('force_kwargs', {})
        fig_axis = shap.plots.force(
            shape_values,
            show=False,
            matplotlib=True,
            **force_kwargs
        )
        return fig_axis
    def _plot_bar(self,shap_values,*args,**kwargs):
        fig_axis = shap.plots.bar(kwargs.get("complete_shap_values",None),
                                  show = False, 
                       max_display=kwargs.get('max_display',None))
        return fig_axis
    
    def _plot_bees(self,shape_values,*args,**kwargs):
        bees_kwargs = kwargs.get("bees_kwargs",{})

        fig_axis = shap.plots.beeswarm(kwargs.get("complete_shap_values",None),
                                       show = False,
                                       max_display = kwargs.get("max_display",None),
                                       **bees_kwargs)
        return fig_axis
    
    def _plot_scatter(self,shape_values,feature_name = None,*args,**kwargs):
        if not feature_name:
            raise ValueError("No feature name specified")
        
        complete_shap_values = kwargs.get("complete_shap_values",None)
        scatter_kwargs = kwargs.get("scatter_kwargs",{})
        scatter_color_by_feature = kwargs.get("scatter_color_by_feature",{})
        if scatter_color_by_feature:
            color = complete_shap_values[:,scatter_color_by_feature]
        complete_shap_values = complete_shap_values[:,feature_name]
        _, fig_axis = plt.subplots()
        shap.plots.scatter(complete_shap_values, ax=fig_axis,
                           show=False,color = color, **scatter_kwargs)
        return fig_axis
    
    def __str__(self):
        return f"Shape Explainer for {self.out_model_name}"