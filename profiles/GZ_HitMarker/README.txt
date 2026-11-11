GZ_HitMarker - hit markers and hit/kill sounds for the shooter, headgear knocked off by a headshot kill
Settings: GZ_HitMarker.json in this folder. Read on server start.
Delete the file and the mod creates it again with default values. Errors go to script_*.log with the [GZ_HitMarker] prefix.
A value outside its range is moved to the nearest limit and a WARNING is written to the log.
A key missing from the file uses its default value; for FlyOffSlots that is an empty list (nothing flies off).

MARKERS (true / false)
  HitmarkersOnPlayers    markers for hits on players. Default true.
  HitmarkersOnInfected   markers for hits on infected. Default true.
  HitmarkersOnAnimals    markers for hits on animals. Default true.
  MeleeHitmarkers        markers and sounds for melee hits (knife, axe, fists). Default true.
  A disabled marker also disables the sound of that hit.

HEADGEAR FLY-OFF (players and infected; animals have none)
  HeadgearFlyOff         true/false  a headshot kill knocks off items from the FlyOffSlots slots. Default true.
  HeadgearFlyOffOnMelee  true/false  the same for a melee headshot kill. Default true.
  FlyOffSlots            list of slots in quotes: "Headgear", "Mask", "Eyewear". Default ["Headgear"].
  FlyUpForce             number 0-200, upward throw force. Default 20.
  FlyAwayForce           number 0-200, throw force away from the shooter. Default 12.
  FlySpin                number 0-50, spin in flight, rad/s (0 - no spin). Default 9.

WHICH SOUND PLAYS (only the shooter hears it; 4 variants per kind, except melee and kill)
  headshot kill (helmet does not matter)                  -> Headshot
  kill in any other body part                             -> Kill (muffled bell)
  melee hit                                               -> Melee
  bullet in the head of a player in a helmet, still alive -> Helmet
  bullet in the torso of a player in a body armor vest    -> Armor
  everything else, and any hit on infected and animals    -> Body
  A ruined helmet or vest does not count as armor.

  ArmorThreshold         number 0-1. An item in the helmet or vest slot counts as armor if it lets through
                         no more than this share of bullet damage. Default 0.8. Vanilla values:
                           vests: plate carrier 0.3, police and press 0.5, Chestplate 0.55
                           helmets: military (Mich, Gorka, SSh-68, ballistic) 0.25, pilot 0.5,
                           moto and firefighter 0.75, hockey, construction, skate and fur headdresses 0.9

VOLUME (number 0-2: 0 - off, 1 - as is). Default 1, KillSoundVolume 0.2.
  BodyHitSoundVolume     Body
  ArmorHitSoundVolume    Armor
  HelmetHitSoundVolume   Helmet
  MeleeHitSoundVolume    Melee
  KillSoundVolume        Kill
  HeadshotSoundVolume    Headshot

OTHER
  DebugLog               true/false  log every hit (target, zone, sound) and headgear fly-off. Keep false on a live server. Default false.
  ConfigVersion          internal, do not change.

==========================================================================================

GZ_HitMarker — хит-маркеры и звуки попаданий/убийств у стрелка, срыв головного убора при убийстве в голову
Настройки: GZ_HitMarker.json в этой папке. Читается при старте сервера.
Удалите файл — мод создаст его заново со значениями по умолчанию. Ошибки пишутся в script_*.log с префиксом [GZ_HitMarker].
Значение вне диапазона исправляется до ближайшей границы, в лог пишется WARNING.
Ключа нет в файле — действует значение по умолчанию; для FlyOffSlots это пустой список (ничего не слетает).

МАРКЕРЫ (true / false)
  HitmarkersOnPlayers    маркеры при попадании по игрокам. По умолчанию true.
  HitmarkersOnInfected   маркеры при попадании по заражённым. По умолчанию true.
  HitmarkersOnAnimals    маркеры при попадании по животным. По умолчанию true.
  MeleeHitmarkers        маркеры и звуки за удары в ближнем бою (нож, топор, кулаки). По умолчанию true.
  Выключенный маркер выключает и звук этого попадания.

СРЫВ ГОЛОВНОГО УБОРА (игроки и заражённые; у животных нет)
  HeadgearFlyOff         true/false  убийство в голову срывает вещи из слотов FlyOffSlots. По умолчанию true.
  HeadgearFlyOffOnMelee  true/false  то же при убийстве в голову ударом в ближнем бою. По умолчанию true.
  FlyOffSlots            список слотов в кавычках: "Headgear", "Mask", "Eyewear". По умолчанию ["Headgear"].
  FlyUpForce             число 0-200, сила броска вверх. По умолчанию 20.
  FlyAwayForce           число 0-200, сила броска от стрелка. По умолчанию 12.
  FlySpin                число 0-50, вращение в полёте, рад/с (0 — без вращения). По умолчанию 9.

КАКОЙ ЗВУК ИГРАЕТ (слышит только стрелок; у каждого вида 4 варианта, кроме удара и убийства)
  убийство в голову (шлем не важен)                -> Headshot
  убийство в другую часть тела                     -> Kill (глухой колокольчик)
  удар в ближнем бою                               -> Melee
  пуля в голову игрока в шлеме, игрок жив          -> Helmet
  пуля в туловище игрока в бронежилете             -> Armor
  всё остальное, а также любые попадания по зомби и животным -> Body
  Испорченный (ruined) шлем или жилет бронёй не считается.

  ArmorThreshold         число 0-1. Вещь в слоте шлема или жилета считается бронёй, если пропускает не больше
                         этой доли урона пули. По умолчанию 0.8. Ванильные значения:
                           жилеты: плитник 0.3, полицейский и пресс 0.5, Chestplate 0.55
                           шлемы: военные (Mich, Горка, СШ-68, баллистический) 0.25, пилотский 0.5,
                           мото и пожарный 0.75, хоккейный, строительный, скейт и шапки из шкур 0.9

ГРОМКОСТЬ (число 0-2: 0 — выкл, 1 — как есть). По умолчанию 1, у KillSoundVolume 0.2.
  BodyHitSoundVolume     Body
  ArmorHitSoundVolume    Armor
  HelmetHitSoundVolume   Helmet
  MeleeHitSoundVolume    Melee
  KillSoundVolume        Kill
  HeadshotSoundVolume    Headshot

ПРОЧЕЕ
  DebugLog               true/false  писать в лог каждое попадание (цель, зона, звук) и срыв убора. На живом сервере — false. По умолчанию false.
  ConfigVersion          служебное, не менять.
