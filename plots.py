import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
import scipy.stats as stats
import db_queries as db

class Plots():

    def __init__(self):
        self.queries = db.Queries()

    def tweet_intensity(self):
        data = self.queries.tweet_intensity()

        x = [int(i[0]) for i in data]
        y = [int(i[1]) for i in data]

        plt.style.use('custom538')

        fig, ax = plt.subplots()
        fig.set_size_inches(8,4)

        ax.plot(y, x)
        ax.set_title("Intensity of tweets")
        ax.set_ylabel("Tweets")
        ax.set_yscale('log')
        ax.set_xlabel("Users")


        plt.tight_layout()
        plt.savefig("figure2.png")
        plt.show()

    def users_by_month(self):
        data = self.queries.users_by_month()
        y = [int(i[1]) for i in data]

        N = 12
        months = (
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
        'December')

        ind = np.arange(N)
        width = 0.35

        fig, ax = plt.subplots()
        # fig.set_size_inches(12, 9)
        rects1 = ax.bar(ind, y, width, color='b')

        ax.set_ylabel("Number of users")
        ax.set_title("Number of users per month")
        ax.set_xticks(ind)
        ax.set_xticklabels(months, rotation=40, ha='center')

        plt.tight_layout()
        plt.savefig('users_by_month.png')
        plt.show()

    def tweets_by_month(self):
        data = self.queries.tweets_by_month()
        y = [int(i[1]) for i in data]

        N = 12
        months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')

        ind = np.arange(N)
        width = 0.35

        fig, ax = plt.subplots()
        #fig.set_size_inches(12, 9)
        rects1 = ax.bar(ind, y, width, color='b')

        ax.set_ylabel("Number of tweets")
        ax.set_title("Number of tweets per month")
        ax.set_xticks(ind)
        ax.set_xticklabels(months, rotation = 40, ha='center')

        plt.tight_layout()
        plt.savefig('tweets_by_month.png')
        plt.show()

    def tweets_and_users_by_month(self):
        data = self.queries.tweets_by_month()
        tweets = [int(i[1]) for i in data]

        data = self.queries.users_by_month()
        users = [int(i[1]) for i in data]

        N = 12
        months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')

        ind = np.arange(N)
        width = 0.4

        plt.style.use('custom538')

        fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2)
        fig.set_size_inches(12, 6)
        rects1 = ax1.bar(ind, tweets, width)

        ax1.set_ylabel("Number of tweets")
        ax1.set_title("Number of tweets per month")
        ax1.set_xticks(ind+width)
        ax1.set_xticklabels(months, rotation = 30, ha='right')
        ax1.set_xticklabels(months)



        rects2 = ax2.bar(ind, users, width)

        ax2.set_ylabel("Number of users")
        ax2.set_title("Number of users per month")
        ax2.set_xticks(ind+width)
        ax2.set_xticklabels(months, rotation=30, ha='right')


        plt.tight_layout()
        plt.savefig('figure3.png')
        plt.show()

    def time_intervals(self):
        data = self.queries.time_intervals()

        x = [int(i[0]) for i in data]
        y = [int(i[1]) for i in data]

        plt.style.use('custom538')

        fig, ax = plt.subplots()
        #fig.set_size_inches(12, 9)
        ax.plot(x, y)

        ax.set_xlabel("Days")
        ax.set_xlim(0, 365)
        ax.set_ylabel("Users")

        ax.set_title("Time intervals")

        plt.tight_layout()
        plt.savefig('figure5.png')
        plt.show()

    def distance_between_tweets_and_pois(self):
        data = self.queries.distance_between_tweets_and_pois()
        y = [float(i[1]) for i in data]
        print(y)

        fig, ax = plt.subplots()
        # fig.set_size_inches(12, 9)
        ax.boxplot(y, 0, '', 0)

        #ax.set_xlabel("days")
        #ax.set_xlim(0, 365)
        #ax.set_ylabel("users")

        ax.set_title("Minimum distance to POIs")

        plt.tight_layout()
        plt.savefig('figure6.png')
        plt.show()

    def time_distribution(self):
        data = self.queries.time_distribution_weekdays()
        weekdays = [int(i[1]) for i in data]

        data = self.queries.time_distribution_weekend()
        weekend = [int(i[1]) for i in data]

        N = 24
        hours = ("00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","10:00", \
                  "12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00")

        ind = np.arange(N)
        width = 0.35

        plt.style.use('custom538')

        fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2)
        fig.set_size_inches(12, 6)

        rects1 = ax1.bar(ind, weekdays, width, label='Weekdays')
        rects1 = ax1.bar(ind+width, weekend, width, label='Weekend', color = '#E24A33')

        ax1.set_ylabel("Number of tweets")
        ax1.set_title("Temporal distribution of tweets")
        ax1.set_xticks(ind+2*width)
        ax1.set_xticklabels(hours, rotation = 30, ha='right', fontsize='9')
        ax1.legend(loc=2)

        data = self.queries.time_distribution_weekdays_near_POI()
        weekdaysP = [int(i[1]) for i in data]
        print(weekdaysP)

        data = self.queries.time_distribution_weekend_near_POI()
        weekendP = [int(i[1]) for i in data]
        print(weekendP)

        rects3 = ax2.bar(ind, weekdaysP, width, label='Weekdays')
        rects4 = ax2.bar(ind + width, weekendP, width, label='Weekend', color = '#E24A33')

        ax2.set_ylabel("Number of tweets")
        ax2.set_title("Temporal distribution of tweets (near POIs)")
        ax2.set_xticks(ind+2*width)
        ax2.set_xticklabels(hours, rotation=30, ha='right', fontsize=9)
        ax2.legend(loc=2)

        plt.tight_layout()
        plt.savefig('figure8.png')
        plt.show()

    def avg_stddev_distance_to_POI(self):
        data = self.queries.avg_stddev_distance_to_POI()

        x = [int(i[0]) for i in data]
        avg = [int(i[1]) for i in data]
        stddev = [int(i[2]) for i in data]

        plt.style.use('custom538')

        fig, ax = plt.subplots()
        fig.set_size_inches(12,6)

        ax.plot(avg, label="Average")
        ax.plot(stddev, label="Standard deviation")
        ax.set_title("Distance to closest POI")
        ax.legend()



        plt.tight_layout()
        plt.savefig("figure6.png")
        plt.show()

    def avg_distance_and_interval(self):
        data = self.queries.avg_distance_and_interval()

        x = [int(i[0]) for i in data]
        y = [int(i[1]) for i in data]

        plt.style.use('custom538')

        fig, ax = plt.subplots()
        fig.set_size_inches(16,16)

        ax.scatter(y, x)
        #ax.set_title("Intensity of tweets")
        ax.set_ylabel("Average distance to closest POI")
        #ax.set_yscale('log')
        ax.set_xlabel("Time interval in days")


        plt.tight_layout()
        plt.savefig("scatter.png")
        plt.show()

    def time_gap_between_consecutive_tweets(self):
        data = self.queries.time_gap_between_consecutive_tweets()

        x = [int(i[0]) for i in data]
        gaps = [int(i[1]) for i in data]

        plt.style.use('custom538')

        fig, ax = plt.subplots()
        fig.set_size_inches(8,8)

        num_bins = 50
        n, bins, patches = ax.hist(gaps, num_bins, normed=1, histtype='step', cumulative=True, linewidth=2)

        """
        r = np.log(gaps).diff().as_matrix()[1:]
        sigma = np.std(r)
        mu = np.mean(r) +0.5*sigma*sigma

        y = mlab.normpdf(bins, mu, sigma).cumsum()
        y /= y[-1]
        ax.plot(bins, y, 'k--', linewidth=1.5)
        """


        ax.set_title("Time gap between consecutive tweets (hours)")
        ax.set_ylabel("% Tweets")
        ax.set_ylim(0.8, 1.0)
        #ax.set_yscale('log')
        ax.set_xlabel("Time gap (hours)")


        plt.tight_layout()
        plt.savefig("figure7.png")
        plt.show()