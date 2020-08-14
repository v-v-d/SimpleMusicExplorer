import Vue from "vue";

const getTimeWithDoubleZero = time => {
  return time < 10 ? `0${time}` : time;
};

Vue.filter("secToHHMMSS", sec => {
  sec = Number(sec);
  const h = getTimeWithDoubleZero(Math.floor(sec / 3600));
  const m = getTimeWithDoubleZero(Math.floor((sec % 3600) / 60));
  const s = getTimeWithDoubleZero(Math.floor((sec % 3600) % 60));

  return h > 0 ? `${h}:${m}:${s}` : `${m}:${s}`;
});
