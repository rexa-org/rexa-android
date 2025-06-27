import React, { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, Text } from 'react-native-paper';

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const handleLogin = () => {
    // TODO: API call for login
    alert('Logged in (dummy)');
  };
  return (
    <View style={{ flex: 1, justifyContent: 'center', padding: 16 }}>
      <TextInput label="Email" value={email} onChangeText={setEmail} autoCapitalize="none" style={{ marginBottom: 8 }} />
      <TextInput label="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 8 }} />
      <Button mode="contained" onPress={handleLogin}>Login</Button>
      <Text style={{ marginTop: 16 }}>Don't have an account? Sign up</Text>
    </View>
  );
} 