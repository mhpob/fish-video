library(dplyr); library(ggplot2); library(gganimate)

data <- read.csv('bsb_vid_tracked.csv') %>%
  select(-X) %>%
  # Try to get speed in pixels/second. Too noisy to show anything. :(
  split(., .$id) %>%
  lapply(., FUN = function(fish){
    for(i in seq_len(nrow(fish) - 1)){
      fish$x_spd[i] <- (fish$pos_x[i + 1] - fish$pos_x[i]) / (1/60)
      fish$y_spd[i] <- (fish$pos_y[i + 1] - fish$pos_y[i]) / (1/60)
    }
    fish
  }) %>%
  bind_rows() %>%
  mutate(x_spd = ifelse(abs(x_spd) > (1920/2), 0, x_spd),
         y_spd = ifelse(abs(y_spd) > (1080/2), 0, y_spd))



ggplot() +
  geom_path(data = data, aes(x = pos_x, y = pos_y, color = frame)) +
  scale_y_reverse()+
  facet_wrap(~id)

ggplot() +
  geom_path(data = data, aes(x = pos_x, y = pos_y, color = id)) +
  scale_y_reverse()


ggplot() +
  geom_path(data = data, aes(x = pos_x, y = pos_y, color = id)) +
  scale_y_reverse() +
  transition_time(frame)+
  ease_aes('linear')

anim_save('bsb_gif.gif')

d2 <- data.frame(pos = c(data$pos_x, data$pos_y),
                 axis = rep(c('x','y'), each = 4668),
                 id = rep(data$id, times = 2),
                 frame = rep(data$frame, times = 2))

ggplot(data = d2, aes(x = frame, y = pos, color = id)) +
  geom_point() +
  geom_smooth() +
  facet_wrap(~axis, nrow = 2, scales = 'free_y')

# Speed (too noisy)
ggplot() +
  geom_point(data = data, aes(x=frame, y = x_spd, color = id))
