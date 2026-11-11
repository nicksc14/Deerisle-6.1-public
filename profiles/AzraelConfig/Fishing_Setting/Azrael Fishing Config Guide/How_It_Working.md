# Azrael Fishing Mod
# HOW IT WORKING

## RU: 
Как происходит процесс рыбалки в моде?

### --- Поиск рыбы

После заброса удочки мод проверяет список рыбы, подходящий для текущего типа воды: море, пруд, река или озеро. Проверка происходит в случайном порядке.

Для каждой рыбы учитываются условия ловли: подходящий крючок, наличие или отсутствие нужной наживки, шанс появления рыбы, модификаторы снастей, специальные зоны и другие параметры. Первая рыба, которая успешно проходит все проверки, выбирается как цель.

После выбора цели начинается ожидание сигнала клёва. Каждый цикл действия, когда прокручивается колесо прогресса, происходит попытка показать сигнал - всплеск воды.

Когда появился всплеск, нужно вовремя подсечь рыбу: отпустить ЛКМ во время сигнала. Если вы успели, начнётся мини-игра по вытягиванию рыбы. Если не успели - рыба уйдёт, а к снастям могут примениться штрафы в зависимости от настроек.


### --- Мини-игра

После успешной подсечки откроется интерфейс мини-игры.

В верхней части интерфейса находится основная шкала прогресса вытягивания (1 в UI_Guide.png). Если прогресс заполнится до конца - рыба будет поймана. Если прогресс упадёт до нуля - рыба сорвётся.

Сначала вы увидите уменьшающуюся синюю полоску (2). Это таймер безопасного завершения рыбалки. Он нужен на случай, если вы поняли, что рыба слишком сильная или снасти не выдержат. Если завершить мини-игру до окончания синего таймера, штрафы будут минимальными: например, потеря крючка или небольшой урон снастям. Эти последствия можно настроить в конфиге.

Когда синий таймер закончится, появится красная полоска (2). Это основной таймер вытягивания рыбы. Если он закончится раньше, чем вы поймаете рыбу, она сорвётся. В этом случае штрафы будут серьёзнее: урон снаряжению, потеря крючка, обрыв лески и другие последствия в зависимости от настроек.

В центре интерфейса находится широкая серая шкала (3). По ней движется иконка рыбы (4). Ваша задача - удерживать иконку рыбы внутри рамки захвата (5).

Управление простое:

- удерживайте ЛКМ, чтобы двигать рамку захвата вправо;
- отпускайте ЛКМ, чтобы рамка двигалась влево;
- старайтесь держать иконку рыбы внутри рамки.

Пока рыба находится внутри рамки захвата, прогресс вытягивания увеличивается. Если рыба находится вне рамки, прогресс начинает снижаться. Чем сложнее рыба, тем быстрее она двигается, чаще меняет направление и тем труднее удерживать её в рамке.

Слева от основной шкалы находятся индикаторы нагрузки снаряжения (6): удочки, крючка, катушки и лески.

Если рыба тяжелее, чем максимально допустимая нагрузка конкретного элемента снаряжения, этот элемент начинает перегружаться. Когда иконка рыбы находится внутри рамки захвата, нагрузка быстро растёт. Индикатор постепенно поднимается и меняет цвет на красный.

Если индикатор нагрузки достигнет максимума, соответствующий элемент снаряжения сломается, а рыба сорвётся.

Однако перегруз не всегда означает мгновенный проигрыш. Если рыба находится вне рамки захвата, нагрузка на снаряжение начинает снижаться. Благодаря этому в некоторых ситуациях можно рискнуть и вытащить рыбу, которая тяжелее допустимого веса снастей. Для этого нужно аккуратно чередовать удержание рыбы в рамке и короткие моменты сброса нагрузки.

Таким образом, мини-игра строится не только на удержании рыбы в рамке, но и на контроле риска: чем тяжелее и сильнее рыба, тем важнее правильно выбирать снасти и следить за перегрузкой.



## EN: 
How does the fishing process work in the mod?

### --- Finding a fish

After you cast the fishing rod, the mod checks the fish list suitable for the current water type: sea, pond, river, or lake. The check is performed in random order.

For each fish, the mod takes fishing conditions into account: suitable hook, required bait or no bait, fish spawn chance, equipment modifiers, special zones, and other parameters. The first fish that successfully passes all checks is selected as the target.

After the target is selected, the mod starts waiting for a bite signal. During each action cycle, when the progress wheel rotates, the mod attempts to show a signal - a water splash.

When the splash appears, you need to hook the fish in time by releasing LMB during the signal. If you do it in time, the fish pulling mini-game will start. If you miss the timing, the fish will escape, and penalties may be applied to your equipment depending on the settings.


### --- Mini-game

After successfully hooking the fish, the mini-game interface will open.

At the top of the interface, you will see the main pulling progress bar (1 in UI_Guide.png). If the progress reaches the maximum, the fish is caught. If the progress drops to zero, the fish escapes.

At first, you will see a decreasing blue bar. This is the safe release timer. It is used when you realize that the fish is too strong or your equipment may not handle it. If you end the mini-game before the blue timer runs out, the penalties will be minimal: for example, losing a hook or taking minor equipment damage. These consequences can be adjusted in the config.

When the blue timer ends, a red bar will appear. This is the main fish pulling timer. If it runs out before you catch the fish, the fish will escape. In this case, the penalties will be more serious: equipment damage, hook loss, line break, and other consequences depending on the settings.

In the center of the interface, there is a wide gray bar. The fish icon moves along this bar. Your goal is to keep the fish icon inside the capture frame.

The controls are simple:

- hold LMB to move the capture frame to the right;
- release LMB to move the capture frame to the left;
- try to keep the fish icon inside the frame.

While the fish is inside the capture frame, the pulling progress increases. If the fish is outside the frame, the progress starts to decrease. The more difficult the fish is, the faster it moves, the more often it changes direction, and the harder it is to keep it inside the frame.

To the left of the main bar, there are equipment load indicators: rod, hook, reel, and line.

If the fish is heavier than the maximum allowed load of a specific equipment part, that part starts to overload. When the fish icon is inside the capture frame, the load increases quickly. The indicator rises and gradually changes color to red.

If the load indicator reaches the maximum, the corresponding equipment part breaks, and the fish escapes.

However, overload does not always mean an instant failure. If the fish is outside the capture frame, the equipment load starts to decrease. Because of this, in some situations you can take a risk and pull out a fish that is heavier than your equipment is normally able to handle. To do this, you need to carefully alternate between keeping the fish inside the frame and briefly letting the load drop.

This means the mini-game is not only about keeping the fish inside the frame, but also about risk control: the heavier and stronger the fish is, the more important it becomes to choose the right equipment and manage overload carefully.
