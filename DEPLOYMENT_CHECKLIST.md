# Deployment Checklist for marketing.aureolegroup.com

## Pre-Deployment

- [ ] DNS configured: `marketing.aureolegroup.com` points to server IP
- [ ] Firewall rules: Ports 80 and 443 are open
- [ ] SSL certificates obtained (if using HTTPS)

## Docker Setup

1. **Build and start containers:**
   ```bash
   sudo docker compose up --build -d
   ```

2. **Check container status:**
   ```bash
   sudo docker compose ps
   ```

3. **View logs:**
   ```bash
   sudo docker compose logs -f
   ```

## Port Configuration

The nginx container should be mapped to:
- Port 80 (HTTP) → Host port 80
- Port 443 (HTTPS) → Host port 443

**Important:** Make sure no other service is using ports 80/443 on the host.

## SSL Certificate Setup

### Option 1: Using Let's Encrypt (Recommended)

1. **Install certbot:**
   ```bash
   sudo apt-get update
   sudo apt-get install certbot
   ```

2. **Obtain certificate:**
   ```bash
   sudo certbot certonly --standalone -d marketing.aureolegroup.com
   ```

3. **Certificates will be in:**
   ```
   /etc/letsencrypt/live/marketing.aureolegroup.com/
   ```

4. **Update nginx.conf:**
   - Uncomment HTTPS server block
   - Uncomment HTTP redirect block
   - Comment out HTTP server block

5. **Restart nginx:**
   ```bash
   sudo docker compose restart nginx
   ```

### Option 2: Self-Signed Certificate (Testing Only)

```bash
sudo mkdir -p /etc/letsencrypt/live/marketing.aureolegroup.com/
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/letsencrypt/live/marketing.aureolegroup.com/privkey.pem \
  -out /etc/letsencrypt/live/marketing.aureolegroup.com/fullchain.pem
```

## Testing

1. **Test HTTP:**
   ```bash
   curl -I http://marketing.aureolegroup.com
   ```

2. **Test HTTPS (if configured):**
   ```bash
   curl -I https://marketing.aureolegroup.com
   ```

3. **Test from browser:**
   - Open: `http://marketing.aureolegroup.com` or `https://marketing.aureolegroup.com`

## Troubleshooting

### Port Already in Use

If you get "port already in use" error:

```bash
# Check what's using port 80
sudo lsof -i :80

# Check what's using port 443
sudo lsof -i :443

# Stop conflicting service (e.g., Apache)
sudo systemctl stop apache2
# OR
sudo systemctl stop nginx
```

### Nginx Not Starting

```bash
# Check nginx logs
sudo docker compose logs nginx

# Test nginx configuration
sudo docker compose exec nginx nginx -t
```

### Can't Access Domain

1. **Check DNS:**
   ```bash
   nslookup marketing.aureolegroup.com
   dig marketing.aureolegroup.com
   ```

2. **Check firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

3. **Check if containers are running:**
   ```bash
   sudo docker compose ps
   ```

### SSL Certificate Issues

```bash
# Check if certificates exist
sudo ls -la /etc/letsencrypt/live/marketing.aureolegroup.com/

# Verify certificate
sudo openssl x509 -in /etc/letsencrypt/live/marketing.aureolegroup.com/fullchain.pem -text -noout
```

## Post-Deployment

- [ ] Website accessible via domain
- [ ] Static files loading correctly
- [ ] Media files accessible
- [ ] HRMS login working
- [ ] SSL certificate valid (if using HTTPS)
- [ ] Auto-renewal configured for SSL (if using Let's Encrypt)

## Auto-Renewal for Let's Encrypt

Add to crontab:
```bash
sudo crontab -e
```

Add line:
```
0 0 * * * certbot renew --quiet && docker compose restart nginx
```

