import matplotlib.pyplot as plt
import numpy as np
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

        ax.plot(x, y)
        ax.set_title("Tweet intensity")
        ax.set_ylabel("Number of users")
        ax.set_yscale('log')
        ax.set_xlabel("Tweets")


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

        ax.set_xlabel("days")
        ax.set_xlim(0, 365)
        ax.set_ylabel("users")

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

        rects1 = ax1.bar(ind, weekdays, width, color='b')
        rects1 = ax1.bar(ind+width, weekend, width, color='r')

        ax1.set_ylabel("Number of tweets")
        ax1.set_title("Time distribution")
        ax1.set_xticks(ind+width)
        ax1.set_xticklabels(hours, rotation = 30, ha='center')

        data = self.queries.time_distribution_weekdays_near_POI()
        weekdaysP = [int(i[1]) for i in data]
        print(weekdaysP)

        data = self.queries.time_distribution_weekend_near_POI()
        weekendP = [int(i[1]) for i in data]
        print(weekendP)

        rects3 = ax2.bar(ind, weekdaysP, width, color='b')
        rects4 = ax2.bar(ind + width, weekendP, width, color='r')

        ax2.set_ylabel("Number of tweets")
        ax2.set_title("Time distribution (near POIs)")
        ax2.set_xticks(ind + width)
        ax2.set_xticklabels(hours, rotation=30, ha='center')

        plt.tight_layout()
        plt.savefig('figure8.png')
        plt.show()