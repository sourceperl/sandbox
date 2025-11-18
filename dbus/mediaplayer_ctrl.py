""" MPRIS Player Control via D-Bus: Play/Pause Toggle """

# sudo apt install python-dbus (test with v1.3.2)
import dbus

try:
    # 1. connect to the Session Bus (where media players usually run)
    bus = dbus.SessionBus()

    # 2. find an active MPRIS service name
    # MPRIS names follow the pattern 'org.mpris.MediaPlayer2.PlayerName'
    names = bus.list_names()
    mpris_services = [name for name in names or [] if name.startswith('org.mpris.MediaPlayer2.')]

    if not mpris_services:
        raise RuntimeError('no active MPRIS media player found on the D-Bus session')

    # use the first player found
    player_service_name = mpris_services[0]
    print(f'found media player: {player_service_name}')

    # 3. get the object path for the player interface
    player_proxy = bus.get_object(player_service_name, '/org/mpris/MediaPlayer2')

    # 4. get the standard MPRIS Player interface
    mpris_interface = dbus.Interface(player_proxy, dbus_interface='org.mpris.MediaPlayer2.Player')

    # 5. call the desired method dynamically, method names are case-sensitive (e.g., Play, Pause, Next)
    play = getattr(mpris_interface, 'Play')
    play_pause = getattr(mpris_interface, 'PlayPause')
    pause = getattr(mpris_interface, 'Pause')
    next = getattr(mpris_interface, 'Next')
    previous = getattr(mpris_interface, 'Previous')
    stop = getattr(mpris_interface, 'Stop')
    play_pause()
    print('command sent successfully')
except dbus.exceptions.DBusException as e:
    print(f'error controlling media player via D-Bus: {e}')
except AttributeError:
    print(f'error: The player does not support the command')
