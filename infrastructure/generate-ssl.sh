#!/bin/bash
# ============================================================================
# SSL Certificate Generation Script
# Generates self-signed SSL certificates for local HTTPS
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create ssl directory if it doesn't exist
mkdir -p ssl

echo -e "${YELLOW}Generating self-signed SSL certificate for local use...${NC}"

# Generate private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Household/OU=IT/CN=meal-planner.local" \
    -addext "subjectAltName=DNS:meal-planner.local,DNS:localhost,IP:192.168.1.100"

# Set correct permissions
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem

echo -e "${GREEN}✓ SSL certificate generated successfully!${NC}"
echo -e "${YELLOW}Certificate location:${NC} ssl/cert.pem"
echo -e "${YELLOW}Private key location:${NC} ssl/key.pem"
echo ""
echo -e "${YELLOW}To trust this certificate on your devices:${NC}"
echo -e "  ${GREEN}macOS:${NC} Open Keychain Access, import cert.pem, mark as trusted"
echo -e "  ${GREEN}Windows:${NC} Double-click cert.pem, install to 'Trusted Root Certification Authorities'"
echo -e "  ${GREEN}Linux:${NC} sudo cp ssl/cert.pem /usr/local/share/ca-certificates/meal-planner.crt && sudo update-ca-certificates"
echo -e "  ${GREEN}iOS/Android:${NC} Email cert.pem to device, open and install"
echo ""
echo -e "${YELLOW}Note:${NC} This is a self-signed certificate for local use only."
echo -e "      Browsers will show a security warning until you trust it."
