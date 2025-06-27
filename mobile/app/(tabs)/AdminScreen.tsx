import React from 'react';
import { View } from 'react-native';
import { Text, Card } from 'react-native-paper';

const dummyCommission = 123.45;
const dummyModeration = [
  { id: 1, title: 'Pending Reward 1' },
  { id: 2, title: 'Pending Reward 2' },
];

export default function AdminScreen() {
  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Card style={{ marginBottom: 16 }}>
        <Card.Title title="Commission Report" />
        <Card.Content>
          <Text>Total Commission: ₹{dummyCommission}</Text>
        </Card.Content>
      </Card>
      <Text variant="titleMedium" style={{ marginBottom: 8 }}>Moderation Queue</Text>
      {dummyModeration.map(r => (
        <Card key={r.id} style={{ marginBottom: 8 }}>
          <Card.Content>
            <Text>{r.title}</Text>
          </Card.Content>
        </Card>
      ))}
    </View>
  );
} 