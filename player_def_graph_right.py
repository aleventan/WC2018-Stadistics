import json
import pandas as pd
from game_def import teamList, getIdMatch

class NvoJson:
    def __init__(self, archivo_json, lista):
        self.archivo_json = archivo_json
        self.lista = lista

    def ordenar_y_guardar(self):
        with open(self.archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        for elemento in self.lista:
            sorted_data = sorted(datos, key=lambda x: x[elemento], reverse=True)
            top_20 = sorted_data[:20]

            top_20_datos = [{'player_name': x['player_name'], 'player_nickname': x['player_nickname'], 'match_played': x['match_played'],
                             elemento: x[elemento], 'team_name': x['team_name']} for x in top_20]

            nombre_nuevo_archivo = elemento + '_top20.json'
            with open(nombre_nuevo_archivo, 'w', encoding='utf-8') as f:
                try:
                    json.dump(top_20_datos, f, ensure_ascii=False, indent=4)
                    print('Archivo ' + nombre_nuevo_archivo + ' creado')
                except Exception as e: print(e)


list_elements = ['total_shots', 'total_shots_on_target_pl', 'total_goals_pl', 'total_assists_pl', 'total_passes_pl', 'total_dribble_complete_pl',
                 'total_cross_complete_pl', 'total_interc_won_pl', 'total_blocks_pl', 'total_fouls_won_pl']
all_fw = NvoJson('all_pl.json', list_elements)
all_fw.ordenar_y_guardar()