import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';

export const Button = ({ title, onPress, variant = 'primary', disabled }) => {
  const buttonStyles = {
    primary: {
      backgroundColor: colors.accent,
      color: colors.white
    },
    secondary: {
      backgroundColor: colors.secondary,
      color: colors.white
    },
    outline: {
      backgroundColor: 'transparent',
      borderColor: colors.accent,
      borderWidth: 1,
      color: colors.accent
    }
  };

  const currentStyle = buttonStyles[variant];

  return (
    <TouchableOpacity 
      style={[styles.button, { backgroundColor: currentStyle.backgroundColor }, disabled && styles.disabled]} 
      onPress={onPress}
      disabled={disabled}
    >
      <Text style={[styles.text, { color: currentStyle.color }]}>{title}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: typography.sizes.body,
    fontWeight: typography.weights.medium,
  },
  disabled: {
    opacity: 0.6,
  }
});