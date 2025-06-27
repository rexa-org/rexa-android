import React, { useState, useCallback } from 'react';
import { View, FlatList, RefreshControl } from 'react-native';
import { Text, Card, Button } from 'react-native-paper';

const dummyRewards = [
  { id: 1, title: 'GPay Cashback', app: 'GPay', value: 50, expiry: '2024-12-31' },
  { id: 2, title: 'PhonePe Voucher', app: 'PhonePe', value: 100, expiry: '2024-11-15' },
];

export default function HomeScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [rewards, setRewards] = useState(dummyRewards);

  const onRefresh = useCallback(() => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1000);
  }, []);

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <FlatList
        data={rewards}
        keyExtractor={item => item.id.toString()}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        renderItem={({ item }) => (
          <Card style={{ marginBottom: 12 }}>
            <Card.Title title={item.title} subtitle={item.app} />
            <Card.Content>
              <Text>Value: ₹{item.value}</Text>
              <Text>Expiry: {item.expiry}</Text>
            </Card.Content>
          </Card>
        )}
      />
    </View>
  );
} 