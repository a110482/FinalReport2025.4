from ViewModel import ViewModel
from MainView import MainView

if __name__ == "__main__":
    view_model = ViewModel()
    main_view = MainView()
    main_view.bind_view_model(view_model=view_model)
    main_view.run()