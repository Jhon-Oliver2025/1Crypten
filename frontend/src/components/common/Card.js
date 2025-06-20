import React from 'react';
import { View, StyleSheet } from 'react-native';
import { colors } from '../../theme/colors';

export const Card = ({ children, style }) => {
  return (
    <View style={[styles.card, style]}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.secondary,
    borderRadius: 12,
    padding: 16,
    marginVertical: 8,
    shadowColor: colors.primary,
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  }
});