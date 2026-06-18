class Solution {
public:
    double angleClock(int hour, int minutes) {
        // 1 hour = 30 degrees, 1 minute khisakne par hour hand 0.5 degree chalta hai
        double hourAngle = (hour % 12) * 30.0 + minutes * 0.5;
        
        // 1 minute = 6 degrees
        double minuteAngle = minutes * 6.0;
        
        // Absolute difference
        double angle = abs(hourAngle - minuteAngle);
        
        // Smaller angle chahiye
        return min(angle, 360.0 - angle);
    }
};