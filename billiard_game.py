import time
import math
import platform

# Cek sistem operasi untuk fungsi input keyboard
is_windows = platform.system() == "Windows"
if is_windows:
    import msvcrt
else:
    import sys
    import tty
    import termios

from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# --- Fungsi Input Keyboard Realtime ---
def get_key():
    """Membaca satu karakter dari keyboard tanpa perlu menekan Enter."""
    if is_windows:
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
        return None
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            import select
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                ch = sys.stdin.read(1)
            else:
                ch = None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# --- Fungsi Utama ---
def run_billiard_game():
    print("Script Python berjalan. Cek jendela CoppeliaSim untuk instruksi.")

    # Koneksi ke Coppeliasim
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    
    sim.stopSimulation()
    time.sleep(1)
    sim.startSimulation()

    # Pengambilan Handle Objek
    try:
        cue_ball = sim.getObject('/Sphere[6]')
        aiming_line = sim.getObject('/AimingLine')
        
        all_balls = [cue_ball]
        for i in range(6):
            ball = sim.getObject(f'/Sphere[{i}]')
            all_balls.append(ball)

    except Exception as e:
        error_msg = f"Gagal mendapatkan handle objek. Pastikan nama benar."
        print(f"{error_msg} ({e})")
        sim.addStatusbarMessage(error_msg)
        return

    instructions = "GILIRAN ANDA --- A/D: Arah | W/S: Kekuatan | Spasi: Tembak"
    sim.addStatusbarMessage(instructions)

    # Loop Game Utama
    is_aiming = True
    angle = 0.0
    power = 50.0

    while True:
        if is_aiming:
            key = get_key()
            
            angle_changed = False
            if key == 'd':
                angle -= 0.05
                angle_changed = True
            elif key == 'a':
                angle += 0.05
                angle_changed = True
            elif key == 'w':
                power = min(100.0, power + 2)
            elif key == 's':
                power = max(0.0, power - 2)

            if angle_changed:
                angle = angle % (2 * math.pi)

            cue_ball_pos = sim.getObjectPosition(cue_ball, sim.handle_world)
            sim.setObjectPosition(aiming_line, cue_ball_pos, sim.handle_world)
            sim.setObjectOrientation(aiming_line, [0, 0, angle], sim.handle_world)

            scale_x = 0.5 + power / 100.0
            sim.scaleObject(aiming_line, scale_x, 1.0, 1.0, 0)
            
            status_message = f"Angle: {math.degrees(angle):.1f} | Power: {power:.0f}%"
            sim.addStatusbarMessage(status_message)

            if key == ' ':
                sim.addStatusbarMessage("Tembak!")
                MAX_FORCE = 100
                force_magnitude = (power / 100.0) * MAX_FORCE
                force_vector = [math.cos(angle) * force_magnitude, math.sin(angle) * force_magnitude, 0]
                sim.addForceAndTorque(cue_ball, force_vector, [0, 0, 0])
                sim.scaleObject(aiming_line, 0.0001, 1.0, 1.0, 0)
                is_aiming = False
                sim.addStatusbarMessage("... Menunggu semua bola berhenti...")

        else:
            total_velocity = 0.0
            for ball in all_balls:
                lin_vel, ang_vel = sim.getObjectVelocity(ball)
                total_velocity += sum(v*v for v in lin_vel)
            
            if total_velocity < 0.01:
                time.sleep(1)
                sim.addStatusbarMessage(instructions)
                power = 50.0
                is_aiming = True
        
        time.sleep(0.02)

if __name__ == '__main__':
    try:
        run_billiard_game()
    except KeyboardInterrupt:
        print("\nGame dihentikan oleh pengguna.")
    finally:
        try:
            client = RemoteAPIClient()
            sim = client.getObject('sim')
            sim.addStatusbarMessage("Koneksi script Python terputus.")
            sim.stopSimulation()
        except:
            pass