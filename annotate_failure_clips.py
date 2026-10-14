from pathlib import Path
import cv2
import numpy as np


SOURCE_DIR = Path('/home/jia064/Downloads')
OUTPUT_DIR = Path(__file__).parent / 'assets' / 'annotated_failure_clips'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CASES = {
    1: {
        'type': 'Planner / navigation deadlock candidate',
        'reason': 'Barrier pocket ahead; little net progress in this short clip',
        'confidence': 'Moderate visual match',
        'ellipse': (960, 680, 390, 250),
    },
    2: {
        'type': 'Planner / navigation deadlock candidate',
        'reason': 'Blocked corridor ahead; repeated view with little net progress',
        'confidence': 'Moderate visual match',
        'ellipse': (960, 680, 390, 250),
    },
    3: {
        'type': 'Planner / navigation deadlock candidate',
        'reason': 'Robot turns toward a barrier pocket, then makes no clear escape',
        'confidence': 'Strong visual match',
        'ellipse': (970, 660, 420, 250),
    },
    4: {
        'type': 'Planner / navigation deadlock candidate',
        'reason': 'Fence blocks the forward view; motion is mainly a small reorientation',
        'confidence': 'Moderate visual match',
        'ellipse': (980, 650, 500, 270),
    },
    5: {
        'type': 'Planner / navigation deadlock candidate',
        'reason': 'Fabric barrier remains directly ahead with negligible net motion',
        'confidence': 'Moderate visual match',
        'ellipse': (920, 680, 430, 260),
    },
    6: {
        'type': 'Planner / navigation deadlock candidate',
        'reason': 'Narrow barrier configuration persists for 16 s without clear progress',
        'confidence': 'Strong visual match',
        'ellipse': (980, 650, 440, 270),
    },
}


def translucent_box(frame, p1, p2, color=(245, 245, 245), alpha=0.88):
    overlay = frame.copy()
    cv2.rectangle(overlay, p1, p2, color, -1, cv2.LINE_AA)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


def dashed_ellipse(frame, center, axes, color, thickness=5, dash=18):
    for start in range(0, 360, dash * 2):
        cv2.ellipse(frame, center, axes, 0, start, start + dash, color,
                    thickness, cv2.LINE_AA)


def annotate(frame, case):
    h, w = frame.shape[:2]
    scale = w / 1920.0
    red = (35, 35, 210)
    blue = (205, 85, 20)
    green = (55, 125, 35)

    cx, cy, ax, ay = case['ellipse']
    center = (round(cx * scale), round(cy * scale))
    axes = (round(ax * scale), round(ay * scale))
    dashed_ellipse(frame, center, axes, red, max(2, round(5 * scale)))

    translucent_box(frame, (round(30 * scale), round(25 * scale)),
                    (round(1160 * scale), round(170 * scale)))
    cv2.rectangle(frame, (round(30 * scale), round(25 * scale)),
                  (round(1160 * scale), round(170 * scale)), red,
                  max(2, round(3 * scale)), cv2.LINE_AA)
    cv2.putText(frame, 'MATCHED FAILURE TYPE', (round(60 * scale), round(78 * scale)),
                cv2.FONT_HERSHEY_DUPLEX, 1.05 * scale, red,
                max(2, round(2 * scale)), cv2.LINE_AA)
    cv2.putText(frame, case['type'], (round(60 * scale), round(135 * scale)),
                cv2.FONT_HERSHEY_DUPLEX, 1.15 * scale, (20, 20, 20),
                max(2, round(2 * scale)), cv2.LINE_AA)

    translucent_box(frame, (round(30 * scale), round(190 * scale)),
                    (round(1170 * scale), round(330 * scale)))
    cv2.rectangle(frame, (round(30 * scale), round(190 * scale)),
                  (round(1170 * scale), round(330 * scale)), blue,
                  max(2, round(3 * scale)), cv2.LINE_AA)
    cv2.putText(frame, 'VISIBLE EVIDENCE', (round(60 * scale), round(245 * scale)),
                cv2.FONT_HERSHEY_DUPLEX, 0.95 * scale, blue,
                max(2, round(2 * scale)), cv2.LINE_AA)
    cv2.putText(frame, case['reason'], (round(60 * scale), round(300 * scale)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.82 * scale, (20, 20, 20),
                max(1, round(2 * scale)), cv2.LINE_AA)

    translucent_box(frame, (round(30 * scale), h - round(150 * scale)),
                    (w - round(30 * scale), h - round(25 * scale)))
    cv2.rectangle(frame, (round(30 * scale), h - round(150 * scale)),
                  (w - round(30 * scale), h - round(25 * scale)), green,
                  max(2, round(3 * scale)), cv2.LINE_AA)
    cv2.putText(frame, f"Assessment: {case['confidence']}",
                (round(60 * scale), h - round(96 * scale)),
                cv2.FONT_HERSHEY_DUPLEX, 0.9 * scale, green,
                max(2, round(2 * scale)), cv2.LINE_AA)
    cv2.putText(frame, 'Camera evidence alone cannot confirm planner state or physical contact.',
                (round(60 * scale), h - round(52 * scale)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.72 * scale, (20, 20, 20),
                max(1, round(2 * scale)), cv2.LINE_AA)
    return frame


for number, case in CASES.items():
    source = SOURCE_DIR / f'download ({number}).mp4'
    target = OUTPUT_DIR / f'clip_{number:02d}_annotated.mp4'
    cap = cv2.VideoCapture(str(source))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(str(target), cv2.VideoWriter_fourcc(*'mp4v'),
                             fps, (width, height))
    if not cap.isOpened() or not writer.isOpened():
        raise RuntimeError(f'Could not process {source}')
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        writer.write(annotate(frame, case))
        count += 1
    cap.release()
    writer.release()
    print(f'{source.name} -> {target.name} ({count} frames)')
