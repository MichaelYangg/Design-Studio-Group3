import request from '../utils/request';

export const fetchMonthlyData = monthlyquery => {
    return request({
        url: '/monthly/',
        method: 'get',
        params: monthlyquery
    });
};