import pandas as pd

# STEP 설정
# RED
# YELLOW
# LEFT
# GREEN
# 0, 1

df = pd.DataFrame(
    {'STEP': [0, 1, 2, 3, 4, 5, 6, 7], 'RED': [1, 1, 1, 1, 1, 1, 1, 1], 'YELLOW': [0, 0, 0, 1, 0, 0, 0, 0],
     'LEFT': [1, 1, 1, 0, 0, 0, 0, 0], 'GREEN': [0, 0, 0, 0, 0, 0, 0, 0]})
df = df.set_index('STEP')
df.to_csv("test.csv")
# 예시
# STEP 0 = RED 1, YELLOW 0, LEFT 1, GREEN 0
# 스텝 0은 빨간불과 좌회전이 들어오게 해야한다