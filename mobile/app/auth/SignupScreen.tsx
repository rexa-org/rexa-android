import React, { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, Text } from 'react-native-paper';

export default function SignupScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const handleSignup = () => {
    // TODO: API call for signup
    alert('Signed up (dummy)');
  };
  return (
    <View style={{ flex: 1, justifyContent: 'center', padding: 16 }}>
      <TextInput label="Email" value={email} onChangeText={setEmail} autoCapitalize="none" style={{ marginBottom: 8 }} />
      <TextInput label="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 8 }} />
      <Button mode="contained" onPress={handleSignup}>Sign Up</Button>
      <Text style={{ marginTop: 16 }}>Already have an account? Login</Text>
    </View>
  );
} 