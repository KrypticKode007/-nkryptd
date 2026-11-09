[BUILD] STEP 1/7: FROM python:3.11-slim AS builder
[BUILD] STEP 2/7: WORKDIR /compiler_box
[BUILD] STEP 3/7: COPY requirements.txt . && pip install --no-cache-dir --user -r requirements.txt
[BUILD] STEP 4/7: FROM python:3.11-slim AS runner
[BUILD] STEP 5/7: RUN groupadd -g 10002 defense_group && useradd -r -u 10002 -g defense_group defense_user
[BUILD] STEP 6/7: COPY --from=builder /root/.local /home/defense_user/.local
[BUILD] STEP 7/7: ENV PATH=/home/defense_user/.local/bin:$PATH
[HEALTHCHECK] Running local security validation string check...
[HEALTHCHECK] Input validation matches baseline output payload signature cleanly.
[STATUS] SUCCESS: Container successfully locked down to user ID 10002 (defense_user).
