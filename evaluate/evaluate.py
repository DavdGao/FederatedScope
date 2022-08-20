# coding=utf-8
import collections
import json
import numpy as np
import sys

# 错误字典，这里只是示例
error_msg = {
    1: "Bad input file",
    2: "Wrong input file format",
    3: "The number of predictions is wrong"
}


def dump_2_json(info, path):
    with open(path, 'w') as output_json_file:
        json.dump(info, output_json_file)


def report_error_msg(detail, showMsg, out_p):
    error_dict = dict()
    error_dict['errorDetail'] = detail
    error_dict['errorMsg'] = showMsg
    error_dict['score'] = 0
    error_dict['scoreJson'] = {}
    error_dict['success'] = False
    dump_2_json(error_dict, out_p)


def report_score(score, score_client, out_p):
    result = dict()
    result['success'] = True
    result['score'] = score

    # 这里{}里面的score注意保留，但可以增加其他key，比如这样：
    # result['scoreJson'] = {'score': score, 'aaaa': 0.1}
    result['scoreJson'] = {'score': score, 'score_client': score_client}

    dump_2_json(result, out_p)


def get_acc(predict, label):
    return float(sum(predict == label) / len(label))


def get_mse(predict, label):
    return np.mean(np.power(predict - label, 2))


def load_file(path):
    data = collections.defaultdict(list)
    with open(path, 'r') as file:
        for line in file:
            row = list()
            try:
                for i, _ in enumerate(line.replace(' ', '').split(',')):
                    if i < 2:
                        row.append(int(_))
                    else:
                        row.append(float(_))
            except ValueError:
                raise ValueError('Please check the value within the prediction.')

            data[row[0]].append(row[1:])

            if len(row) != dimensions[row[0] - 1] + 2:
                raise ValueError(
                    f'The number of prediction of Client #{row[0]} is wrong (expect {dimensions[row[0] - 1] + 2}, get {len(row)})')

    # check the index of the client
    if set(data.keys()) != set([_ + 1 for _ in range(num_client)]):
        raise ValueError('Please check the index of the client, which should start with 1.')

    # sort the data by predict_id within the data of each client
    for key, value in data.items():
        data[key] = np.array(sorted(value, key=lambda x: x[0]))[:, 1:]

    return data


# Contest related parameters
num_client = 13
task_client = ['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'r', 'r', 'r', 'r', 'r']
num_samples = [417, 61, 740, 34, 63, 367, 743, 260, 44902, 36465, 756, 203, 23550]
dimensions = [1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 12]
# base_client = [0.7362110311750599, 0.7103825136612022, 0.6445945945945946, 0.823529411764706, 0.6031746031746033,
#                0.7384196185286104, 0.6976222521310005, 0.7884615384615384, 0.059199466666666666, 0.0070826566999999995,
#                0.73401082, 1.3613260333333332, 0.004389330833333333]
# base_client = [1-0.736211, 1-0.710383, 1-0.644595, 1-0.823529, 1-0.603175, 1-0.738420, 1-0.697622, 1-0.788462, 0.059199, 0.007083, 0.734011, 1.361326, 0.004389]
base_client = [0.263789, 0.289617, 0.355404, 0.176471, 0.396825, 0.261580, 0.302378, 0.211538, 0.059199, 0.007083,
               0.734011, 1.361326, 0.004389]

def calculate(submit_path):
    standard_path = '/mnt/gaodawei.gdw/FederatedScope/evaluate/ground_truth_labels.csv'
    # submit_path = '/mnt/gaodawei.gdw/FederatedScope/exp/client4_batch25_samelr_/prediction.csv'

    out_path = 'result.txt'

    try:
        # Read ground truth labels here for each client
        labels = load_file(standard_path)

        predicts = load_file(submit_path)

        imp_ratio = 0.
        imp_ratio_clients = list()
        metrics = list()
        for idx, (task, num_sample, base) in enumerate(zip(task_client, num_samples, base_client)):
            client_id = idx + 1

            # obtain both labels and predicts of the current client
            client_labels = labels[client_id]
            client_predicts = predicts[client_id]

            # check the number of predictions for each client
            if len(client_labels) != len(client_predicts):
                msg = f'The number of predictions for client #{idx + 1} is wrong (expect {len(client_labels)}, but get {len(client_predicts)}).'
                raise Exception(msg)

            if task == 'r':
                metric = get_mse(client_predicts, client_labels)
                indicator = -1.
            else:
                metric = 1 - get_acc(client_predicts, client_labels)
                indicator = -1.

            ir = indicator * (metric - base) / base * 100.
            metrics.append(metric)
            imp_ratio_clients.append(ir)
            imp_ratio += ir / float(num_client)

        # Report evaluation results
        print(f"The improve ratio of each client is {imp_ratio_clients}.")
        print(f"The performance of each client is {metrics}.")
        print(imp_ratio)
        # report_score(imp_ratio, imp_ratio_clients, out_path)
    except Exception as e:
        report_error_msg(repr(e), repr(e), out_path)


if __name__ == '__main__':
    for _ in [
        '/mnt/gaodawei.gdw/FederatedScope/exp/client1_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client2_grad05_round200_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client4_batch25_samelr_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client1_12twoepoch_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client2_grad05_round200_repeat_addepoch_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client2modeldouble_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client3_lowerlrforlargeclient_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client5_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client1_12twoepoch_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client3_lowerlrforlargeclient_/prediction.csv',
        '/mnt/gaodawei.gdw/FederatedScope/exp/client4_batch25_samelr_/prediction.csv',


    ]:
        calculate(_)
        print('-'*10)