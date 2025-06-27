import React, { useState } from 'react';
import { View } from 'react-native';
import { Text, Card, Button, SegmentedButtons } from 'react-native-paper';

const dummyListings = [
  { id: 1, title: 'GPay Cashback', type: 'Free', price: 0 },
  { id: 2, title: 'PhonePe Voucher', type: 'Points', price: 100 },
  { id: 3, title: 'Paytm Card', type: 'Paid', price: 50 },
];

export default function MarketplaceScreen() {
  const [filter, setFilter] = useState('All');
  const filtered = filter === 'All' ? dummyListings : dummyListings.filter(l => l.type === filter);
  return (
    <View style={{ flex: 1, padding: 16 }}>
      <SegmentedButtons
        value={filter}
        onValueChange={setFilter}
        buttons={[
          { value: 'All', label: 'All' },
          { value: 'Free', label: 'Free' },
          { value: 'Points', label: 'Points' },
          { value: 'Paid', label: 'Paid' },
        ]}
        style={{ marginBottom: 16 }}
      />
      {filtered.map(item => (
        <Card key={item.id} style={{ marginBottom: 12 }}>
          <Card.Title title={item.title} subtitle={item.type} />
          <Card.Content>
            <Text>Price: {item.price === 0 ? 'Free' : `₹${item.price}`}</Text>
            <Button mode="contained" style={{ marginTop: 8 }}>Claim</Button>
          </Card.Content>
        </Card>
      ))}
    </View>
  );
} 