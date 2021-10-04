from .model import pso_run


def setup_application_callbacks(model, view):
    view.set_run_callback(
        lambda *args, model=model, view=view, **kwargs: _run(model=model, view=view)
    )

    for (input_name, attr_name, dtype) in [
        ('gen', 'n_generations', int),
        ('pop_size', 'population_size', int),
        ('inertia', 'inertia', float),
        ('cog', 'cognitive', float),
        ('soc', 'social', float),
        ('seed', 'seed', int),
    ]:
        callback = lambda v, model=model, name=attr_name, dtype=dtype: _update_model(model, name, v, dtype)
        view.set_input_changed_callback(input_name, callback)
        view.set_input_value(input_name, getattr(model, attr_name))


def _update_model(model, attr_name, new_value, dtype):
    try:
        new_value = dtype(new_value)
    except ValueError:
        new_value = 0
    setattr(model, attr_name, new_value)


def _run(model, view):
    # TODO: Show generation feedback somewhere on GUI
    def _pso_run_callback(i, pop):
        view.disable_run_button()
        try:
            view.update_canvas(pop)
        finally:
            view.enable_run_button()

    pso_run(model, _pso_run_callback)
