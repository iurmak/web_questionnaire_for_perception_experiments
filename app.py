from flask import Flask, render_template, request, redirect, url_for
from time import strftime, gmtime
from calendar import timegm

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def website():
    if request.method == 'GET':
        word_stimuli = [(1, 'but.wav', ((1, 'обувь'), (2, 'было (глагол)'))),
                        (2, 'vaz.wav', ((1, 'овца'), (2, 'коза'))),
                        (3, 'kut.wav', ((1, 'собака'), (2, 'короткий'))),
                        (4, 'nedz.wav', ((1, 'нос'), (2, 'игла'))),
                        (5, 'kud.wav', ((1, 'собака'), (2, 'короткий'))),
                        (6, 'but.wav', ((1, 'обувь'), (2, 'было (глагол)'))),
                        (7, 'par.wav', ((1, 'крыло'), (2, 'огонь'))),
                        (8, 'duzd.wav', ((1, 'друг'), (2, 'вор'))),
                        (9, 'kud voiced final cons.wav', ((1, 'собака'), (2, 'короткий'))),
                        (10, 'nedz.wav', ((1, 'нос'), (2, 'игла'))),
                        (11, 'yed.wav', ((1, 'открытый'), (2, 'мост'))),
                        (12, 'xiz.wav', ((1, 'правый, справа'), (2, 'шить'))),
                        (13, 'yet.wav', ((1, 'открытый'), (2, 'мост'))),
                        (14, 'kut with short aspiration.wav', ((1, 'короткий'), (2, 'собака'))),
                        (15, 'duzd.wav', ((1, 'друг'), (2, 'вор'))),
                        (16, 'yet with short aspiration.wav', ((1, 'открытый'), (2, 'мост'))),
                        (17, 'nedz.wav', ((1, 'нос'), (2, 'игла'))),
                        (18, 'yed voiced final cons.wav', ((1, 'открытый'), (2, 'мост'))),
                        (19, 'kut with long vowel.wav', ((1, 'короткий'), (2, 'собака'))),
                        (20, 'par.wav', ((1, 'крыло'), (2, 'огонь'))),
                        (21, 'kut with short vowel.wav', ((1, 'короткий'), (2, 'собака'))),
                        (22, 'duzd.wav', ((1, 'друг'), (2, 'вор'))),
                        (23, 'yet with long vowel.wav', ((1, 'открытый'), (2, 'мост'))),
                        (24, 'vaz.wav', ((1, 'овца'), (2, 'коза'))),
                        (25, 'yet with short vowel.wav', ((1, 'открытый'), (2, 'мост'))),
                        (26, 'but.wav', ((1, 'обувь'), (2, 'было (глагол)')))
                        ]
        paired_stimuli = [(27, 'yet yed.wav', ((1, 'мост'), (2, 'открытый'))),
                        (28, 'kud kut.wav', ((1, 'короткий'), (2, 'собака'))),
                        (29, 'nedz par.wav', ((1, 'крыло'), (2, 'нос'))),
                        (30, 'xiz but.wav', ((1, 'правый, справа'), (2, 'обувь'))),
                        (31, 'yed yet.wav', ((1, 'мост'), (2, 'открытый'))),
                        (32, 'duzd vaz.wav', ((1, 'коза'), (2, 'вор'))),
                        (33, 'nedz par.wav', ((1, 'крыло'), (2, 'нос'))),
                        (34, 'kut kud.wav', ((1, 'короткий'), (2, 'собака'))),
                        (35, 'but nedz.wav', ((1, 'нос'), (2, 'обувь'))),
                        (36, 'yet_sh yet.wav', ((1, 'мост'), (2, 'открытый'))),
                        (37, 'vaz nedz.wav', ((1, 'коза'), (2, 'нос'))),
                        (38, 'but vaz.wav', ((1, 'обувь'), (2, 'коза'))),
                        (39, 'kut kut_sh.wav', ((1, 'короткий'), (2, 'собака'))),
                        (40, 'duzd par.wav', ((1, 'крыло'), (2, 'вор'))),
                        (41, 'but nedz.wav', ((1, 'нос'), (2, 'обувь'))),
                        (42, 'kut_sh_v kut_l_v.wav', ((1, 'короткий'), (2, 'собака'))),
                        (43, 'duzd vaz.wav', ((1, 'коза'), (2, 'вор'))),
                        (44, 'yet_l_v yet_sh_v.wav', ((1, 'мост'), (2, 'открытый')))
                        ]
        return render_template('experiment.html',
                               word_stimuli=word_stimuli,
                               paired_stimuli=paired_stimuli)

    elif request.method == 'POST':
        final_results = {}
        starting_moments = {}
        name = request.form.get('name')
        date = strftime('%d_%m_%Y_%H_%M', gmtime(timegm(gmtime())+10800))
        results = request.form.get('results_dict')[1:].split('%')
        print(results)
        for r in results:
            if '_' in r.split(';')[0]:
                final_results[r.split(';')[0].split('_')[0]] = (r.split(';')[0].split('_')[-1], float(r.split(';')[-1]))
            else:
                starting_moments[r.split(';')[0]] = float(r.split(';')[-1])
        with open(f'static/results/{name}_{date}.tsv', 'w', encoding='utf-8') as f:
            for r in final_results:
                print(r, final_results, final_results.get(r), final_results.get(r)[0], final_results.get(r)[-1])
                if starting_moments.get(r[0], None):
                    s_m = starting_moments.get(r, None)
                    delta = final_results.get(r)[-1] - s_m
                else:
                    delta = None
                f.write('\t'.join([str(r), str(final_results.get(r)[0]), str(starting_moments.get(r, None)), str(final_results.get(r)[-1]), str(delta)]) + '\n')
        return redirect(url_for('website'))




if __name__ == '__main__':
    app.run()
