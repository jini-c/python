import tkinter as tk
from tkinter import messagebox
import random

# ---------------- 점수 생성 함수 ----------------

def generate_tenth_frame():
    throws = []
    first = random.randint(0, 10)
    throws.append(first)
    if first == 10:
        second = random.randint(0, 10)
        throws.append(second)
        if second == 10:
            third = random.randint(0, 10)
            throws.append(third)
    else:
        second = random.randint(0, 10 - first)
        throws.append(second)
        if first + second == 10:
            third = random.randint(0, 10)
            throws.append(third)
    return throws

def generate_frame():
    first = random.randint(0, 10)
    if first == 10:
        return [10]
    second = random.randint(0, 10 - first)
    return [first, second]

def create_player_frames():
    frames = []
    for _ in range(9):
        frames.append({"throws": generate_frame()})
    frames.append({"throws": generate_tenth_frame()})
    return frames

def calculate_score(frames):
    total = 0
    for i in range(10):
        throws = frames[i]["throws"]
        if i == 9:
            score = sum(throws)
        elif len(throws) == 1 and throws[0] == 10:
            bonus = []
            j = i + 1
            while len(bonus) < 2 and j < 10:
                bonus.extend(frames[j]["throws"])
                j += 1
            score = 10 + sum(bonus[:2])
        elif sum(throws) == 10:
            next_throw = frames[i + 1]["throws"][0] if i + 1 < 10 else 0
            score = 10 + next_throw
        else:
            score = sum(throws)
        frames[i]["score"] = score
        total += score
        frames[i]["total"] = total
    return frames

# ---------------- GUI 클래스 ----------------

class BowlingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("볼링 점수 입력기")
        self.name_entries = []

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="플레이어 수를 입력하세요:").pack()
        self.num_players_entry = tk.Entry(self.root)
        self.num_players_entry.pack()

        self.confirm_button = tk.Button(self.root, text="확인", command=self.generate_name_inputs)
        self.confirm_button.pack()

        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack()

        self.start_button = tk.Button(self.root, text="시작", command=self.get_player_names)
        self.start_button.pack()
        self.start_button.config(state=tk.DISABLED)

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

    def generate_name_inputs(self):
        for widget in self.name_frame.winfo_children():
            widget.destroy()
        self.name_entries.clear()

        try:
            num_players = int(self.num_players_entry.get())
            if num_players <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("오류", "올바른 숫자를 입력하세요.")
            return

        for i in range(num_players):
            tk.Label(self.name_frame, text=f"{i+1}번 플레이어 이름:").pack()
            entry = tk.Entry(self.name_frame)
            entry.pack()
            self.name_entries.append(entry)

        self.start_button.config(state=tk.NORMAL)

    def get_player_names(self):
        players = [entry.get().strip() for entry in self.name_entries]
        if "" in players:
            messagebox.showerror("오류", "모든 이름을 입력해주세요.")
            return

        player_scores = {}

        for name in players:
            frames = create_player_frames()
            frames = calculate_score(frames)
            player_scores[name] = frames

        # 기존 결과 제거
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # 결과 출력
        for name, frames in player_scores.items():
            tk.Label(self.result_frame, text=f"🏆 {name} 점수", font=("Arial", 12, "bold")).pack()

            frame_grid = tk.Frame(self.result_frame)
            frame_grid.pack(pady=5)

            for i, frame in enumerate(frames):
                throws_str = f"({', '.join(map(str, frame['throws']))})"
                frame_str = f"{i+1}F\n{throws_str}\n점수:{frame['score']}\n누적:{frame['total']}"
                
                row = 0 if i < 5 else 1
                col = i % 5

                tk.Label(
                    frame_grid,
                    text=frame_str,
                    borderwidth=1,
                    relief="solid",
                    width=18,
                    height=4,
                    font=("Arial", 9)
                ).grid(row=row, column=col, padx=4, pady=4)

            tk.Label(self.result_frame, text="-" * 80).pack(pady=(0, 10))

        messagebox.showinfo("점수 생성 완료", "결과가 화면에 표시되었습니다.")

# ---------------- 실행부 ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = BowlingApp(root)
    root.mainloop()
