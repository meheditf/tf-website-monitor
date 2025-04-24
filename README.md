# Monitoring Stack

This repository contains a monitoring stack using Prometheus, Grafana, Node Exporter, and Blackbox Exporter to monitor various services and system metrics.

## Components

1. **Prometheus** - Time series database and monitoring system
   - Port: 9090
   - Configuration: `prometheus/prometheus.yml`

2. **Grafana** - Visualization and dashboard platform
   - Port: 3010
   - Default credentials:
     - Username: admin
     - Password: secret

3. **Node Exporter** - System metrics exporter
   - Port: 9100
   - Collects CPU, memory, disk, and network metrics

4. **Blackbox Exporter** - HTTP/HTTPS monitoring
   - Port: 9115
   - Configuration: `blackbox/config.yml`

## Monitored Services
- Github Site (https://github.com)
- Linkedin (https://linkedin.com)
- Facebook (https://facebook.com)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Monitoring
   ```

2. Start the monitoring stack:
   ```bash
   docker-compose up -d
   ```

3. Access the services:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3010
   - Node Exporter metrics: http://localhost:9100/metrics
   - Blackbox Exporter: http://localhost:9115

## Configuration

### Prometheus Configuration
- Located in `prometheus/prometheus.yml`
- Scrapes metrics from Node Exporter and Blackbox Exporter
- Monitors HTTP endpoints for availability

### Blackbox Configuration
- Located in `blackbox/config.yml`
- Configures HTTP/HTTPS probe settings
- Uses http_2xx module for endpoint monitoring

### Node Exporter Configuration
- Collects system metrics from the host
- Mounts necessary system directories
- Excludes certain mount points from filesystem metrics

## Monitoring Features

1. **System Metrics**
   - CPU usage
   - Memory utilization
   - Disk I/O
   - Network traffic
   - System load

2. **Service Monitoring**
   - HTTP/HTTPS endpoint availability
   - Response time
   - Status codes
   - SSL certificate validity

## Maintenance

### Updating Configuration
1. Modify the respective configuration files
2. Reload Prometheus configuration:
   ```bash
   curl -X POST http://localhost:9090/-/reload
   ```

### Adding New Services
1. Add new targets to `prometheus/prometheus.yml`
2. Reload Prometheus configuration

### Backup
- Grafana data is persisted in a Docker volume
- Configuration files are version controlled

## Troubleshooting

1. **No Data in Grafana**
   - Check if Prometheus targets are up
   - Verify network connectivity between services
   - Check service logs: `docker-compose logs <service-name>`

2. **Service Not Responding**
   - Check if the service is running: `docker-compose ps`
   - View service logs: `docker-compose logs <service-name>`
   - Verify port mappings and network configuration

## Security Notes

- Grafana password is set to 'secret' by default - change in production
- Services are running in a dedicated Docker network
- HTTPS endpoints are monitored for certificate validity
- System metrics are collected with read-only access
