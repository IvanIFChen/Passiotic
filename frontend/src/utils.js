export const getItemsForPiRound = (pi, round, items) => {
  const piItems = items.filter(item => item.pi_id === pi);
  const roundPiItems = piItems.filter(item => item.round_id === round);
  return roundPiItems;
};

export const getLatestRoundForPi = (pi, items) => {
  const piItems = items.filter(item => item.pi_id === pi);

  let latestRound = 0;
  for (let item of piItems) {
    if (latestRound < item.round_id) {
      latestRound = item.round_id;
    }
  }

  return latestRound;
};
