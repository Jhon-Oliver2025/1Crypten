import React, { useEffect, useState } from 'react';
import { View, Text, Switch, StyleSheet, Alert } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';
import { settingsApi } from '../services/api';

export const SettingsScreen = () => {
  const [settings, setSettings] = useState({
    signalAlerts: false,
    priceAlerts: false
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await settingsApi.getSettings();
      setSettings(response.data);
    } catch (error) {
      Alert.alert('Error', 'Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (key) => {
    try {
      const newSettings = {
        ...settings,
        [key]: !settings[key]
      };
      await settingsApi.updateSettings(newSettings);
      setSettings(newSettings);
    } catch (error) {
      Alert.alert('Error', 'Failed to update settings');
    }
  };

  if (loading) {
    return null; // ou um componente de loading
  }

  return (
    <View style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Notifications</Text>
        <View style={styles.setting}>
          <Text style={styles.settingText}>Signal Alerts</Text>
          <Switch 
            value={settings.signalAlerts}
            onValueChange={() => handleToggle('signalAlerts')}
            trackColor={{ false: colors.darkGray, true: colors.accent }}
            thumbColor={colors.white}
          />
        </View>
        <View style={styles.setting}>
          <Text style={styles.settingText}>Price Alerts</Text>
          <Switch 
            value={settings.priceAlerts}
            onValueChange={() => handleToggle('priceAlerts')}
            trackColor={{ false: colors.darkGray, true: colors.accent }}
            thumbColor={colors.white}
          />
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.primary,
    padding: 16,
  },
  section: {
    backgroundColor: colors.secondary,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: typography.sizes.h3,
    color: colors.white,
    marginBottom: 16,
  },
  setting: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  settingText: {
    fontSize: typography.sizes.body,
    color: colors.white,
  },
});