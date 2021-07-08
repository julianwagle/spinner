from random import choice
from matplotlib import pyplot
from sys import setrecursionlimit
setrecursionlimit(15000)

class PlaySpinner():
    '''
    The following is a simmulation of roullete games.

    Example Usage A: 
        >>> from spinner import *; PlaySpinner()
    Example Usage B: 
        >>> PlaySpinner()
    '''
    def __init__(self):
        # TODO: Add in multi-bet feature to track both high-low and red-black

        # ADJUST # BELOW # VALUES # FREQUENTLY # FOR # EXPIRAMENTATION # 
        self.desired_return_per_bet = 10
        self.max_daily_spins = 400
        self.table_losses_before_entry = 5
        self.total_days_of_play = 250
        self.desired_wallet = 100000
        # ADJUST # ABOVE # VALUES # FREQUENTLY # FOR # EXPIRAMENTATION # 

        self.max_bet_val = 5000
        self.wallet_starting_val = 10000
        self.wallet_min_auth_val = 1

        self.wallet_total_val = self.wallet_starting_val
        self.eval_wallet_vals = []
        self.sanity_checker_wins = []
        self.sanity_checker_losses = []
        self.sanity_checker_total = []
        self.sanity_checker_deviations = []
        self.previous_bet_sizes = []
        self.total_daily_spins = 0
        self.table_spin_loss_counter = 0
        self.total_days_played = 0

        self.TABLE_SLOTS_ALL = list(range(1, 39))
        self.TABLE_SLOTS_HIGH = list(range(1, 19)) # 1 to 18
        self.TABLE_SLOTS_LOW = list(range(19, 37)) # 19 to 37
        self.TABLE_SLOTS_ZERO = list(range(37, 39)) # 37 to 38
        self.TABLE_SLOTS_RED = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.TABLE_SLOTS_BLACK = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.TABLE_SLOTS_GREEN = [37, 38]

        print("at the casino now.")
        self.sit_at_the_table()
        self.perform_analysis()


    def sit_at_the_table(self): 
        print("sitting at the table.")

        while bool(
                self.wallet_min_auth_val < self.wallet_total_val < self.desired_wallet
            ) and bool(
                self.total_days_played <= self.total_days_of_play
            ):

            table_spin_results = self.watch_the_table_spin()
            self.eval_wallet_vals.append(self.wallet_total_val)
            if isinstance(table_spin_results, int):
                table_spin_loss = bool(table_spin_results > 18)
                self.sanity_checker_total.append(1)

                if table_spin_loss: 
                    self.table_spin_loss_counter += 1
                    self.sanity_checker_losses.append(1)
                else: 
                    self.table_spin_loss_counter = 0
                    self.sanity_checker_wins.append(1)

                time_to_bet = bool(self.table_losses_before_entry == self.table_spin_loss_counter)
                if time_to_bet:
                    # print(f"Its time to bet on spin number {self.total_daily_spins}")
                    self.table_spin_loss_counter = 0
                    self.place_a_bet()


    def watch_the_table_spin(self):
        self.total_daily_spins += 1
        my_day_is_over = bool(self.total_daily_spins > self.max_daily_spins)
        # print(f"watcing the table spin for time number {self.total_daily_spins}")
        if my_day_is_over:
            self.head_home()
        else:
            return int(choice(self.TABLE_SLOTS_ALL))


    def verify_sanity(self):
        print("verifying sanity ...")
        total_spins = sum(self.sanity_checker_total)
        total_wins = sum(self.sanity_checker_wins)
        total_losses = sum(self.sanity_checker_losses)
        assert total_spins == total_wins + total_losses
        winning_frequency = total_wins/total_spins * 100
        estimated_likelyhood_of_winning = len(self.TABLE_SLOTS_HIGH)/len(self.TABLE_SLOTS_ALL) * 100
        deviation_from_standard = estimated_likelyhood_of_winning - winning_frequency
        deviation_from_standard_polished = round(deviation_from_standard,3)
        self.sanity_checker_deviations.append(deviation_from_standard)
        deviation_average = sum(self.sanity_checker_deviations) / len(self.sanity_checker_deviations)
        deviation_average_polished = round(deviation_average,3)
        sanity_check_message = str(f"CURRENT DEVIATION:{deviation_from_standard_polished} AVERAGE DEVIATION:{deviation_average_polished}")
        print(f"i'm only {deviation_average_polished}% insane so far")
        return sanity_check_message


    def determine_bet_size(self):
        # print("determining bet size.")
        sum_of_losses = int(sum(self.previous_bet_sizes))
        desired_back_payment = len(self.previous_bet_sizes) * self.desired_return_per_bet
        bet_size = self.desired_return_per_bet + desired_back_payment + sum_of_losses
        reached_table_max = bool(bet_size > self.max_bet_val)
        if reached_table_max: 
            print("I have reached the table max.")
            self.take_a_fat_l()
        else:
            return bet_size 


    def place_a_bet(self):
        self.verify_sanity()
        print("its betting time!")

        bet_size = self.determine_bet_size()
        if isinstance(bet_size, int):
            
            table_spin_results = self.watch_the_table_spin()    
            if isinstance(table_spin_results, int):
                table_spin_loss = bool(table_spin_results > 18)
                self.sanity_checker_total.append(1)

                if table_spin_loss: 
                    self.sanity_checker_losses.append(1)                    
                    self.wallet_total_val -= bet_size
                    self.previous_bet_sizes.append(bet_size)
                    print(f"I lost --${bet_size}--")
                    return self.place_a_bet()
                else: 
                    self.sanity_checker_wins.append(1)                    
                    self.wallet_total_val += bet_size
                    self.previous_bet_sizes = []
                    print(f"I won ++${bet_size}++")
                    return self.sit_at_the_table()


    def take_a_fat_l(self):
        print("taking a fat l.")
        self.table_spin_loss_counter = 0
        self.previous_bet_sizes = []
        return self.sit_at_the_table()


    def head_home(self):
        self.previous_bet_sizes = []
        self.total_daily_spins = 0
        self.table_spin_loss_counter = 0
        self.total_days_played += 1
        # Time to go back to 'work' now ...
        self.sit_at_the_table()


    def perform_analysis(self):
        total_gains = self.wallet_total_val - self.wallet_starting_val
        average_daily_return = total_gains / self.total_days_of_play
        print(self.verify_sanity())
        print(f"Your wallet is at ${self.wallet_total_val}. You received an average daily return of ${average_daily_return}")
        pyplot.plot(self.eval_wallet_vals)
        pyplot.axhline(y = self.wallet_starting_val, color = 'b', linestyle = 'dashed')
        pyplot.axhline(y = self.desired_wallet, color = 'g', linestyle = 'dashed')
        pyplot.axhline(y = self.wallet_min_auth_val, color = 'r', linestyle = 'dashed')
        pyplot.title('Game Evaluation')
        pyplot.xlabel('Time')
        pyplot.ylabel('$hmoney')
        pyplot.show()
