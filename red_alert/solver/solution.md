# Red Alert

## Intended (Alert system)
 1. Login using your credentials
 1. Goto the alert page and goto the admin tab
 1. Copy the contents of **alert_admin.json** into the configuration tab. Click save
 1. Run setup_alerts.sh (be sure that the ip address and port are correct)
 1. Go to the alert page and the contact points tab
 1. Open up the "play" conact point and use the "test" button to send the command to the api

### Notes on alerting:
- The default alert configuration should have group wait set to 1s for immediate alerting
- Only alerts to turn on and off the laser are needed to solve
- Alerts need to be grouped by their 'power cycle' by adding a label based on 'cycle'. 

## Alternative (Manual while watching dashboards)
 1. Login using your credentials
 1. Goto the alert page and goto the admin tab
 1. Copy the contents of **alert_admin.json** into the configuration tab. Click save
 1. Go to the dashboards tab and create dashboards to show you range, battery and heat
 1. Open a sepeate tab in your browser and go to alert page and the contact point tab
 1. Watch the dashboard
 1. Manually trigger all the commands using the "test" button in each contact point.


