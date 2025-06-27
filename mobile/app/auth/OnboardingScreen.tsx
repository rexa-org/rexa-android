import React from 'react';
import { View } from 'react-native';
import { Text, Button } from 'react-native-paper';

export default function OnboardingScreen() {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 16 }}>
      <Text variant="headlineMedium" style={{ marginBottom: 16 }}>Welcome to reX</Text>
      <Text style={{ marginBottom: 24 }}>
        Consolidate, exchange, and sell your digital rewards from all your favorite apps. Privacy-first. Battery-friendly.
      </Text>
      <Button mode="contained">Continue</Button>
    </View>
  );
} 