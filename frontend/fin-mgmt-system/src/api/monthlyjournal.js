import request from '../utils/request';

export function fetchMonthlyData(monthlyquery) {
    return request({
        url: '/monthlyjournal/',
        method: 'get',
        params: monthlyquery
    });
};