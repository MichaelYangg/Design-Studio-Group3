import request from '../utils/request';

export function fetchData(query) {
    return request({
        url: '/transactions/',
        method: 'get',
        params: query
    });
};

export function addList(data) {
    return request({
      url: '/transactions/add/',
      method: 'post',
      data: {
            list: [
                {
                    "transaction_id": data.transaction_id,
                    "volume": data.volume,
                    "unit": data.unit,
                    "date_time": data.date_time,
                    "resource": data.resource,
                    "category": data.category,
                    "explanation": data.explanation
                }
            ]
        }
    });
};

 export function editList(data) {
    return request({
        url: '/transactions/change/',
        method: 'put',
        data: {
          list:[
            {
                "transaction_id": data.transaction_id,
                "volume": data.volume,
                "unit": data.unit,
                "date_time": data.date_time,
                "resource": data.resource,
                "category": data.category,
                "explanation": data.explanation
            }
          ]
      }
   });
};

export function deleteList(data) {
   return request({
       url: '/transactions/delete/',
       method: 'delete',
       data
   });
};

export function queryTransaction(transaction_id) {
    return request({
        url: '/transactions/' + transaction_id,
        method: 'get'
    })
}