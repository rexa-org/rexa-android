import React, { useState } from 'react';
import { View } from 'react-native';
import { Text, Switch, Button, Divider } from 'react-native-paper';

export default function ProfileScreen() {
  const [notificationScraper, setNotificationScraper] = useState(false);
  const [smsScraper, setSmsScraper] = useState(false);
  const [accessibilityScraper, setAccessibilityScraper] = useState(false);
  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Text variant="titleMedium">Scraper Permissions</Text>
      <View style={{ flexDirection: 'row', alignItems: 'center', marginVertical: 8 }}>
        <Text style={{ flex: 1 }}>Notification Listener</Text>
        <Switch value={notificationScraper} onValueChange={setNotificationScraper} />
      </View>
      <View style={{ flexDirection: 'row', alignItems: 'center', marginVertical: 8 }}>
        <Text style={{ flex: 1 }}>SMS Reader</Text>
        <Switch value={smsScraper} onValueChange={setSmsScraper} />
      </View>
      <View style={{ flexDirection: 'row', alignItems: 'center', marginVertical: 8 }}>
        <Text style={{ flex: 1 }}>Accessibility Service</Text>
        <Switch value={accessibilityScraper} onValueChange={setAccessibilityScraper} />
      </View>
      <Divider style={{ marginVertical: 16 }} />
      <Button mode="outlined" style={{ marginBottom: 8 }}>Logout</Button>
      <Button mode="contained" buttonColor="#d32f2f">Delete Account</Button>
    </View>
  );
} 