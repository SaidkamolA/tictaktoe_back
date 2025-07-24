from django.urls import path
from .views import NewGameView, MoveView, StateView, CheckWinnerView, ReadyView, JoinView

urlpatterns = [
    path('api/new_game', NewGameView.as_view()),
    path('api/move', MoveView.as_view()),
    path('api/state/<str:game_id>', StateView.as_view()),
    path('api/check_winner/<str:game_id>', CheckWinnerView.as_view()),
    path('api/ready', ReadyView.as_view()),
    path('api/join', JoinView.as_view()),
] 