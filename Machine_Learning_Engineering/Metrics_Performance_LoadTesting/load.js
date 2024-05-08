import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 100 }, // simulate ramp-up of traffic from 0 to target users
    { duration: '5m', target: 100 }, // stay at target users
    { duration: '5s', target: 0 },   // ramp-down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(99)<500'], // 99% of requests must complete below 500 ms
  },
};

const features = [
  "MedInc",
  "HouseAge",
  "AveRooms",
  "AveBedrms",
  "Population",
  "AveOccup",
  "Latitude",
  "Longitude",
]
const fixed = [1, 1, 1, 1, 1, 1, 0, 0]

const randInt = (max) => (Math.floor(Math.random() * max))

const generator = (cacheRate) => {
  const rand = Math.random()
  const input = rand > cacheRate
    ? features.reduce((acc, f) => {
        acc[f] = randInt(20)
        return acc
      }, {})
    : features.reduce((acc, f, idx) => {
        acc[f] = fixed[idx]
        return acc
      }, {})

  return {
    houses: [ input ]
  }
}

const CACHE_RATE = 0.2
const NAMESPACE = 'aquon'
const BASE_URL = `TARGET_URL`;

export default () => {

    const payload = JSON.stringify(generator(CACHE_RATE))
    const predictionResponse = http.post(`${BASE_URL}/bulk-predict`, payload, {
      headers: { 'Content-Type': 'application/json' },
    });
    check(predictionResponse, {
      'prediction responded with 200': (r) => r.status === 200
    })

};
