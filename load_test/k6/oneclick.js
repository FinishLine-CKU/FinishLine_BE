// 원클릭 검사 동시성 부하 테스트 (docs/oneclick_load_test.md 참고)
//
// 라운드 1회 = 동시 사용자 VUS명이 원클릭을 VUS * ITERATIONS번 나눠서 요청한다.
// 요청마다 새 학번(YYYY9011, 9012, ...)을 쓰므로 라운드 안에서는 중복 저장이 생기지 않는다.
// 라운드가 끝나면 기이수과목을 SQL로 삭제한 뒤 다음 라운드를 실행한다.
//
// 동시에 probe 시나리오가 가벼운 API(get_visitor_info)를 2초마다 호출해,
// 원클릭이 워커를 점유하는 동안 다른 API가 얼마나 느려지는지 측정한다.
//
// 실행 (PowerShell):
//   $env:K6_PROMETHEUS_RW_SERVER_URL="http://localhost:9090/api/v1/write"
//   $env:K6_PROMETHEUS_RW_TREND_STATS="p(50),p(95),max"
//   k6 run -o experimental-prometheus-rw -e BASE_URL=http://<테스트 EC2 IP> -e VUS=3 oneclick.js
import http from 'k6/http';
import { check } from 'k6';
import exec from 'k6/execution';

const BASE_URL = __ENV.BASE_URL;
const VUS = parseInt(__ENV.VUS || '1');
const ITERATIONS = parseInt(__ENV.ITERATIONS || '3');       // VU당 평균 요청 수
const LOADTEST_YEAR = __ENV.LOADTEST_YEAR || '2022';
const MAX_USERS = 89;                                       // YYYY9011 ~ YYYY9099

// 원클릭 1건 약 12초, 워커 3개 기준으로 라운드가 끝날 때까지 probe를 유지한다.
const PROBE_SECONDS = __ENV.PROBE_SECONDS || String(ITERATIONS * 12 * Math.ceil(VUS / 3) + 10);

if (!BASE_URL) {
  throw new Error('BASE_URL을 지정하세요. 예: -e BASE_URL=http://<테스트 EC2 IP>');
}
if (VUS * ITERATIONS > MAX_USERS) {
  throw new Error(`VUS * ITERATIONS는 ${MAX_USERS} 이하여야 합니다.`);
}

export const options = {
  scenarios: {
    oneclick: {
      executor: 'shared-iterations',
      vus: VUS,
      iterations: VUS * ITERATIONS,
      maxDuration: '15m',
      exec: 'oneclick',
    },
    probe: {
      executor: 'constant-arrival-rate',
      rate: 1,
      timeUnit: '2s',
      duration: `${PROBE_SECONDS}s`,
      preAllocatedVUs: 10,
      maxVUs: 100,                                         // probe가 워커 대기로 쌓여도 요청이 누락(dropped)되지 않도록
      exec: 'probe',
    },
  },
  summaryTrendStats: ['avg', 'med', 'p(95)', 'max'],
};

export function oneclick() {
  const no = 11 + exec.scenario.iterationInTest;
  const studentId = `${LOADTEST_YEAR}90${String(no).padStart(2, '0')}`;

  const res = http.post(
    `${BASE_URL}/graduation/oneclick_test/`,
    JSON.stringify({ studentId: studentId, studentPW: 'loadtest' }),
    { headers: { 'Content-Type': 'application/json' }, timeout: '180s', tags: { name: 'oneclick_test' } },
  );

  check(res, {
    'oneclick 200': (r) => r.status === 200,
    'oneclick success': (r) => r.status === 200 && r.json('success') === true,
  });
}

export function probe() {
  const res = http.get(`${BASE_URL}/user/get_visitor_info/`, { timeout: '180s', tags: { name: 'get_visitor_info' } });
  check(res, { 'probe 200': (r) => r.status === 200 });
}
