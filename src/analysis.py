from collections import OrderedDict
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from src import data


def gen_wordcloud(data, filename):
    wordcloud = WordCloud(
        background_color='black',
        max_words=500,
        font_path='../font/Arial Unicode.ttf',
        random_state=None,
        prefer_horizontal=0.8
    ).generate_from_frequencies(data)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    wordcloud.to_file(filename)


def process_data(data):
    years = ['2020', '2021', '2022', '2023', '2024']
    processed_data = {}
    for year in years:
        for t in data[year]:
            if t not in processed_data:
                processed_data[t] = []
            processed_data[t].append(data[year].get(t, 0))

    # 排序數據
    sorted_techs = sorted(processed_data.keys(), key=lambda x: processed_data[x][-1], reverse=True)
    sorted_data = OrderedDict((tech, processed_data[tech]) for tech in sorted_techs)

    # 確保所有技術都有五年的數據
    for tech in sorted_data:
        if len(sorted_data[tech]) < 5:
            sorted_data[tech] += [0] * (5 - len(sorted_data[tech]))

    return sorted_data, years


def plot_trend(sorted_data, years):
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette('husl', n_colors=len(sorted_data))

    for i, (tech, values) in enumerate(sorted_data.items()):
        plt.plot(years, values, marker='o', label=tech, color=colors[i])

    plt.title('COSCUP Technology Trends 2020-2024')
    plt.xlabel('Year')
    # plt.yscale('log')
    plt.ylabel('Percentage')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small', ncol=2)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig('./trend.png', dpi=300)
    plt.close()


if __name__ == '__main__':
    # 生成文字雲
    for year in ['2020', '2021', '2022', '2023', '2024']:
        gen_wordcloud(data.data[year], f'./wc_result/coscup-{year}.png')

    # 處理數據
    sorted_data, years = process_data(data.data)

    # 繪製趨勢圖
    plot_trend(sorted_data, years)