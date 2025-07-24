from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .tictactoe_memory import new_game, move, get_state, check_winner, ready_for_new_game, join_game

# Create your views here.

class NewGameView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'Missing user_id'}, status=400)
        game_id, board, current, winner, winner_line = new_game(user_id)
        game = get_state(game_id)
        player_symbol = get_player_symbol(game, user_id)
        return Response({
            'game_id': game_id,
            'board': board,
            'current': current,
            'winner': winner,
            'winner_line': winner_line,
            'player_symbol': player_symbol,
            'connected_X': game.get('connected_X'),
            'connected_O': game.get('connected_O'),
        })

class MoveView(APIView):
    def post(self, request):
        game_id = request.data.get('game_id')
        row = request.data.get('row')
        col = request.data.get('col')
        symbol = request.data.get('symbol')
        if None in (game_id, row, col, symbol):
            return Response({'detail': 'Missing parameters'}, status=400)
        try:
            row = int(row)
            col = int(col)
        except Exception:
            return Response({'detail': 'Invalid coordinates'}, status=400)
        game, error = move(game_id, row, col, symbol)
        if error:
            return Response({'detail': error}, status=400)
        return Response({
            'board': game['board'],
            'current': game['current'],
            'winner': game['winner'],
            'score_X': game['score_X'],
            'score_O': game['score_O'],
            'score_draw': game['score_draw'],
            'ready_X': game['ready_X'],
            'ready_O': game['ready_O'],
            'winner_line': game.get('winner_line'),
            'connected_X': game.get('connected_X'),
            'connected_O': game.get('connected_O'),
        })

class StateView(APIView):
    def get(self, request, game_id):
        user_id = request.GET.get('user_id')
        game = get_state(game_id)
        if not game:
            return Response({'detail': 'Game not found'}, status=404)
        player_symbol = get_player_symbol(game, user_id) if user_id else None
        return Response({
            'board': game['board'],
            'current': game['current'],
            'winner': game['winner'],
            'score_X': game['score_X'],
            'score_O': game['score_O'],
            'score_draw': game['score_draw'],
            'ready_X': game['ready_X'],
            'ready_O': game['ready_O'],
            'winner_line': game.get('winner_line'),
            'connected_X': game.get('connected_X'),
            'connected_O': game.get('connected_O'),
            'player_symbol': player_symbol,
        })

class CheckWinnerView(APIView):
    def get(self, request, game_id):
        game = get_state(game_id)
        if not game:
            return Response({'detail': 'Game not found'}, status=404)
        winner = check_winner(game['board'])
        if winner:
            return Response({'winner': winner})
        elif all(cell is not None for row in game['board'] for cell in row):
            return Response({'winner': 'draw'})
        else:
            return Response({'winner': None})

class ReadyView(APIView):
    def post(self, request):
        game_id = request.data.get('game_id')
        symbol = request.data.get('symbol')
        if not game_id or not symbol:
            return Response({'detail': 'Missing parameters'}, status=400)
        game, error = ready_for_new_game(game_id, symbol)
        if error:
            return Response({'detail': error}, status=400)
        return Response({
            'board': game['board'],
            'current': game['current'],
            'winner': game['winner'],
            'score_X': game['score_X'],
            'score_O': game['score_O'],
            'score_draw': game['score_draw'],
            'ready_X': game['ready_X'],
            'ready_O': game['ready_O'],
            'winner_line': game.get('winner_line'),
            'connected_X': game.get('connected_X'),
            'connected_O': game.get('connected_O'),
        })

class JoinView(APIView):
    def post(self, request):
        game_id = request.data.get('game_id')
        symbol = request.data.get('symbol')
        user_id = request.data.get('user_id')
        if not game_id or not symbol or not user_id:
            return Response({'detail': 'Missing parameters'}, status=400)
        game, error = join_game(game_id, symbol, user_id)
        if error:
            return Response({'detail': error}, status=400)
        player_symbol = get_player_symbol(game, user_id)
        return Response({
            'board': game['board'],
            'current': game['current'],
            'winner': game['winner'],
            'score_X': game['score_X'],
            'score_O': game['score_O'],
            'score_draw': game['score_draw'],
            'ready_X': game['ready_X'],
            'ready_O': game['ready_O'],
            'winner_line': game.get('winner_line'),
            'connected_X': game.get('connected_X'),
            'connected_O': game.get('connected_O'),
            'player_symbol': player_symbol,
        })
