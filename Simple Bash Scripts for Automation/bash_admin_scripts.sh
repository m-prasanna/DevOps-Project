#!/bin/bash

# ============================================
# 1. LOG CLEANUP SCRIPT
# ============================================
# Cleans up old log files to free disk space

cleanup_logs() {
    echo "=== Log Cleanup Script ==="
    
    LOG_DIR="/var/log"
    DAYS_OLD=30
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root (use sudo)"
        return 1
    fi
    
    echo "Searching for log files older than $DAYS_OLD days..."
    
    # Find and delete old log files
    find "$LOG_DIR" -name "*.log" -type f -mtime +$DAYS_OLD -print -delete
    
    # Compress logs older than 7 days
    find "$LOG_DIR" -name "*.log" -type f -mtime +7 ! -name "*.gz" -exec gzip {} \;
    
    echo "Log cleanup completed!"
}

# ============================================
# 2. BACKUP SCRIPT
# ============================================
# Creates compressed backups of important directories

backup_data() {
    echo "=== Data Backup Script ==="
    
    # Configuration
    SOURCE_DIR="$HOME/Documents"
    BACKUP_DIR="$HOME/Backups"
    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_NAME="backup_$DATE.tar.gz"
    
    # Create backup directory if it doesn't exist
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        echo "Created backup directory: $BACKUP_DIR"
    fi
    
    # Check if source directory exists
    if [ ! -d "$SOURCE_DIR" ]; then
        echo "Error: Source directory $SOURCE_DIR does not exist"
        return 1
    fi
    
    echo "Backing up $SOURCE_DIR..."
    echo "Destination: $BACKUP_DIR/$BACKUP_NAME"
    
    # Create compressed backup
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "Backup completed successfully!"
        echo "Backup size: $(du -h "$BACKUP_DIR/$BACKUP_NAME" | cut -f1)"
    else
        echo "Backup failed!"
        return 1
    fi
    
    # Keep only last 5 backups
    echo "Cleaning up old backups (keeping last 5)..."
    ls -t "$BACKUP_DIR"/backup_*.tar.gz | tail -n +6 | xargs -r rm -f
    
    echo "Remaining backups:"
    ls -lh "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null || echo "No backups found"
}

# ============================================
# 3. SYSTEM UPDATE SCRIPT
# ============================================
# Updates system packages (works for apt-based systems)

update_system() {
    echo "=== System Update Script ==="
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root (use sudo)"
        return 1
    fi
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        echo "Updating package lists..."
        apt-get update
        
        echo "Upgrading packages..."
        apt-get upgrade -y
        
        echo "Removing unnecessary packages..."
        apt-get autoremove -y
        
        echo "Cleaning up..."
        apt-get clean
        
    elif command -v yum &> /dev/null; then
        echo "Updating system with yum..."
        yum update -y
        yum clean all
        
    elif command -v dnf &> /dev/null; then
        echo "Updating system with dnf..."
        dnf upgrade -y
        dnf clean all
        
    else
        echo "No supported package manager found"
        return 1
    fi
    
    echo "System update completed!"
}

# ============================================
# 4. DISK USAGE MONITOR
# ============================================
# Monitors disk usage and alerts if threshold exceeded

check_disk_usage() {
    echo "=== Disk Usage Monitor ==="
    
    THRESHOLD=80
    
    echo "Checking disk usage (threshold: $THRESHOLD%)..."
    echo ""
    
    df -h | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{print $5 " " $1 " " $6}' | while read output;
    do
        usage=$(echo $output | awk '{print $1}' | sed 's/%//g')
        partition=$(echo $output | awk '{print $2}')
        mount=$(echo $output | awk '{print $3}')
        
        if [ $usage -ge $THRESHOLD ]; then
            echo "⚠️  WARNING: $partition mounted on $mount is ${usage}% full"
        else
            echo "✓ $partition mounted on $mount: ${usage}% used"
        fi
    done
}

# ============================================
# 5. SERVICE STATUS CHECKER
# ============================================
# Checks status of critical services

check_services() {
    echo "=== Service Status Checker ==="
    
    # List of services to check (customize as needed)
    SERVICES=("ssh" "cron" "nginx" "apache2" "mysql" "postgresql")
    
    for service in "${SERVICES[@]}"; do
        if systemctl list-unit-files | grep -q "^$service.service"; then
            if systemctl is-active --quiet $service; then
                echo "✓ $service is running"
            else
                echo "✗ $service is NOT running"
            fi
        fi
    done
}

# ============================================
# MAIN MENU
# ============================================

show_menu() {
    echo ""
    echo "================================"
    echo "   System Administration Menu"
    echo "================================"
    echo "1. Clean up old log files"
    echo "2. Backup important data"
    echo "3. Update system packages"
    echo "4. Check disk usage"
    echo "5. Check service status"
    echo "6. Run all checks (4+5)"
    echo "7. Exit"
    echo "================================"
}

# Main execution
while true; do
    show_menu
    read -p "Select an option (1-7): " choice
    
    case $choice in
        1) cleanup_logs ;;
        2) backup_data ;;
        3) update_system ;;
        4) check_disk_usage ;;
        5) check_services ;;
        6) check_disk_usage; check_services ;;
        7) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option. Please try again." ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done