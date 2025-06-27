import React, { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, Text, HelperText } from 'react-native-paper';

export default function AddRewardScreen() {
  const [form, setForm] = useState({
    sourceApp: '',
    type: '',
    value: '',
    expiry: '',
    code: '',
    notes: '',
  });
  const handleChange = (k: string, v: string) => setForm(f => ({ ...f, [k]: v }));
  const handleSubmit = () => {
    // TODO: API call to add reward
    alert('Reward added (dummy)');
  };
  return (
    <View style={{ flex: 1, padding: 16 }}>
      <TextInput label="Source App" value={form.sourceApp} onChangeText={v => handleChange('sourceApp', v)} style={{ marginBottom: 8 }} />
      <TextInput label="Type" value={form.type} onChangeText={v => handleChange('type', v)} style={{ marginBottom: 8 }} />
      <TextInput label="Value" value={form.value} onChangeText={v => handleChange('value', v)} keyboardType="numeric" style={{ marginBottom: 8 }} />
      <TextInput label="Expiry Date" value={form.expiry} onChangeText={v => handleChange('expiry', v)} placeholder="YYYY-MM-DD" style={{ marginBottom: 8 }} />
      <TextInput label="Code" value={form.code} onChangeText={v => handleChange('code', v)} style={{ marginBottom: 8 }} />
      <TextInput label="Notes" value={form.notes} onChangeText={v => handleChange('notes', v)} multiline style={{ marginBottom: 8 }} />
      <Button mode="contained" onPress={handleSubmit}>Add Reward</Button>
    </View>
  );
} 