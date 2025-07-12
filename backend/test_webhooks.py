#!/usr/bin/env python
"""
Test script for webhook functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from gamification.models import WebhookConfig
from gamification.services import WebhookService

def test_discord_webhook():
    """Test Discord webhook"""
    print("Testing Discord webhook...")
    
    try:
        webhook = WebhookConfig.objects.get(platform='discord')
        
        # Test payload
        payload = {
            "embeds": [{
                "title": "🎯 Gamification System Test",
                "description": "Testing Discord webhook integration",
                "color": 3447003,  # Blue color
                "fields": [
                    {
                        "name": "Status",
                        "value": "✅ Webhook working correctly",
                        "inline": True
                    },
                    {
                        "name": "System",
                        "value": "Django Backend",
                        "inline": True
                    }
                ]
            }]
        }
        
        success = WebhookService.send_webhook_notification(webhook, payload)
        if success:
            print("✅ Discord webhook test successful!")
        else:
            print("❌ Discord webhook test failed!")
            
    except WebhookConfig.DoesNotExist:
        print("❌ Discord webhook configuration not found")
    except Exception as e:
        print(f"❌ Discord webhook error: {e}")

def test_teams_webhook():
    """Test Microsoft Teams webhook"""
    print("Testing Microsoft Teams webhook...")
    
    try:
        webhook = WebhookConfig.objects.get(platform='teams')
        
        # Test payload
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Gamification System Test",
            "sections": [{
                "activityTitle": "🎯 Gamification System Test",
                "activitySubtitle": "Testing Microsoft Teams webhook integration",
                "facts": [
                    {"name": "Status", "value": "✅ Webhook working correctly"},
                    {"name": "System", "value": "Django Backend"}
                ]
            }]
        }
        
        success = WebhookService.send_webhook_notification(webhook, payload)
        if success:
            print("✅ Microsoft Teams webhook test successful!")
        else:
            print("❌ Microsoft Teams webhook test failed!")
            
    except WebhookConfig.DoesNotExist:
        print("❌ Microsoft Teams webhook configuration not found")
    except Exception as e:
        print(f"❌ Microsoft Teams webhook error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting webhook integration tests...\n")
    
    # Test Discord
    test_discord_webhook()
    print()
    
    # Test Teams
    test_teams_webhook()
    print()
    
    print("✨ Webhook tests completed!")

if __name__ == "__main__":
    main()
