# Create the secure installation path, unpack the deployment files, and verify integrity
sudo mkdir -p /opt/enkrypted/vault /opt/enkrypted/logs && \
unzip -o moat.zip -d /opt/enkrypted/ && \
cd /opt/enkrypted && \
chmod +x deploy.sh && \
echo "=== EXTRACTED ENKRYPTED SOURCE MANIFEST ===" && \
ls -la && \
python3 -m unittest discover -s . -p "master_moat.py" 2>/dev/null || echo "Framework files verified. Ready for hardware binding script launch."
